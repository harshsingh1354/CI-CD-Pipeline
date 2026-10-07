resource "aws_s3_bucket" "demo" {
  bucket = "cicd-demo-bucket-example"
}

resource "aws_s3_bucket_acl" "demo" {
  bucket = aws_s3_bucket.demo.id
  acl    = "public-read"
}

resource "aws_security_group" "demo" {
  name        = "demo-sg"
  description = "Demo security group"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
