terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "2.6.4"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
    profile = "terraform"
    region  = "us-east-1"
}