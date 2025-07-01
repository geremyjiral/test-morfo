resource "aws_db_subnet_group" "default" {
  name       = "main-subnet-group"
  subnet_ids = data.aws_subnets.all.ids
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "all" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_db_instance" "analysis_db" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "15.2"
  instance_class       = "db.t3.micro"
  username             = var.db_username
  password             = var.db_password
  publicly_accessible  = true
  db_subnet_group_name = aws_db_subnet_group.default.name
  skip_final_snapshot  = true
}
