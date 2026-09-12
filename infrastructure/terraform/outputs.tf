output "ingestion_bucket_name" {
  description = "Name of the S3 bucket used for incoming financial files"
  value       = aws_s3_bucket.ingestion.bucket
}

output "ingestion_bucket_arn" {
  description = "ARN of the ingestion S3 bucket"
  value       = aws_s3_bucket.ingestion.arn
}