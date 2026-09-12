output "ingestion_bucket_name" {
  description = "Name of the S3 bucket used for incoming financial files"
  value       = aws_s3_bucket.ingestion.bucket
}

output "ingestion_bucket_arn" {
  description = "ARN of the ingestion S3 bucket"
  value       = aws_s3_bucket.ingestion.arn
}
output "database_endpoint" {
  description = "RDS PostgreSQL endpoint"
  value       = aws_db_instance.postgres.address
}

output "database_port" {
  description = "RDS PostgreSQL port"
  value       = aws_db_instance.postgres.port
}

output "vpc_id" {
  description = "Project VPC ID"
  value       = aws_vpc.main.id
}