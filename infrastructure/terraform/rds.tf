resource "random_password" "database" {
  length  = 24
  special = false
}

resource "aws_db_subnet_group" "main" {
  name = "financial-data-${var.environment}"

  subnet_ids = [
    aws_subnet.private_a.id,
    aws_subnet.private_b.id
  ]

  tags = {
    Name = "financial-data-${var.environment}"
  }
}

resource "aws_db_instance" "postgres" {
  identifier = "financial-data-${var.environment}"

  engine         = "postgres"
  instance_class = "db.t4g.micro"

  allocated_storage = 20
  storage_type      = "gp3"
  storage_encrypted = true

  db_name  = "financial_data"
  username = "financial_app"
  password = random_password.database.result
  port     = 5432

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.database.id]

  publicly_accessible = false
  multi_az            = false

  backup_retention_period = 1

  skip_final_snapshot = true
  deletion_protection = false
  apply_immediately   = true
}