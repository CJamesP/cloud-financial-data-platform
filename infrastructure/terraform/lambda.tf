data "aws_caller_identity" "current" {}


data "archive_file" "s3_processor" {
  type        = "zip"
  source_dir  = "${path.module}/../../build/lambda/s3_processor"
  output_path = "${path.module}/s3_processor.zip"
}


resource "aws_iam_role" "lambda_processor" {
  name = "financial-data-s3-processor-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "lambda.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })
}


resource "aws_iam_role_policy_attachment" "lambda_logging" {
  role       = aws_iam_role.lambda_processor.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}


resource "aws_iam_role_policy_attachment" "lambda_vpc_access" {
  role       = aws_iam_role.lambda_processor.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}


resource "aws_iam_role_policy" "lambda_s3_access" {
  name = "financial-data-s3-read-${var.environment}"
  role = aws_iam_role.lambda_processor.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "s3:GetObject"
        ]

        Resource = "${aws_s3_bucket.ingestion.arn}/incoming/*"
      }
    ]
  })
}


resource "aws_lambda_function" "s3_processor" {
  function_name = "financial-data-s3-processor-${var.environment}"

  filename         = data.archive_file.s3_processor.output_path
  source_code_hash = data.archive_file.s3_processor.output_base64sha256

  role    = aws_iam_role.lambda_processor.arn
  handler = "lambda_function.handler"
  runtime = "python3.13"

  timeout     = 30
  memory_size = 256

  environment {
    variables = {
      DATABASE_URL = "postgresql+psycopg://financial_app:${random_password.database.result}@${aws_db_instance.postgres.address}:5432/financial_data"
    }
  }

  vpc_config {
    subnet_ids = [
      aws_subnet.private_a.id,
      aws_subnet.private_b.id
    ]

    security_group_ids = [
      aws_security_group.lambda.id
    ]
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_logging,
    aws_iam_role_policy_attachment.lambda_vpc_access
  ]
}


resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.s3_processor.function_name
  principal     = "s3.amazonaws.com"

  source_arn     = aws_s3_bucket.ingestion.arn
  source_account = data.aws_caller_identity.current.account_id
}


resource "aws_s3_bucket_notification" "ingestion" {
  bucket = aws_s3_bucket.ingestion.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.s3_processor.arn
    events              = ["s3:ObjectCreated:*"]

    filter_prefix = "incoming/"
    filter_suffix = ".csv"
  }

  depends_on = [
    aws_lambda_permission.allow_s3
  ]
}