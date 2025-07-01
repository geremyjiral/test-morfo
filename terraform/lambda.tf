resource "aws_lambda_function" "image_analyzer" {
  function_name = "image-analysis-function"
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "main.lambda_handler"
  timeout       = 30

  filename         = "lambda.zip"
  source_code_hash = filebase64sha256("lambda.zip")
}
