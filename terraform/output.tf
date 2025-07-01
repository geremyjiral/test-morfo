output "s3_bucket" {
  value = aws_s3_bucket.raw.bucket
}

output "rds_endpoint" {
  value = aws_db_instance.analysis_db.endpoint
}

output "lambda_function_name" {
  value = aws_lambda_function.image_analyzer.function_name
}
