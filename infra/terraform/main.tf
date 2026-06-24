terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Example EKS Cluster setup for the platform
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "codeac-cluster"
  cluster_version = "1.29"

  vpc_id     = "vpc-12345678" # Replace with actual VPC
  subnet_ids = ["subnet-123", "subnet-456"]

  eks_managed_node_groups = {
    general = {
      desired_size = 2
      min_size     = 1
      max_size     = 4

      instance_types = ["t3.large"]
    }
  }
}

# RDS Postgres Database
module "db" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 6.0"

  identifier = "codeac-db"
  
  engine               = "postgres"
  engine_version       = "15"
  family               = "postgres15"
  major_engine_version = "15"
  instance_class       = "db.t4g.large"
  
  allocated_storage = 100
  
  db_name  = "codeac_db"
  username = "codeac"
  port     = 5432
  
  # Note: Security groups and subnets omitted for brevity
}
