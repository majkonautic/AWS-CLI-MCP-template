#!/usr/bin/env python3
"""
Example script demonstrating AWS CLI MCP usage.
This shows how to interact with AWS services through the MCP server.
"""

import asyncio
import json
import os
from typing import Dict, Any

# Example functions showing common AWS operations

async def list_s3_buckets():
    """Example: List all S3 buckets"""
    print("📦 Listing S3 buckets...")
    # This would be called through MCP: aws_cli(command="s3api list-buckets")
    
async def list_ec2_instances(region: str = "us-east-1"):
    """Example: List EC2 instances in a region"""
    print(f"🖥️  Listing EC2 instances in {region}...")
    # This would be called through MCP: aws_cli(command="ec2 describe-instances", region=region)

async def get_lambda_functions():
    """Example: List Lambda functions"""
    print("⚡ Listing Lambda functions...")
    # This would be called through MCP: aws_cli(command="lambda list-functions")

async def describe_dynamodb_tables():
    """Example: List DynamoDB tables"""
    print("🗄️  Listing DynamoDB tables...")
    # This would be called through MCP: aws_cli(command="dynamodb list-tables")

async def get_cloudformation_stacks():
    """Example: List CloudFormation stacks"""
    print("📚 Listing CloudFormation stacks...")
    # This would be called through MCP: aws_cli(command="cloudformation list-stacks")

# Example of safe operations
SAFE_EXAMPLES = {
    "List S3 Buckets": {
        "command": "s3api list-buckets",
        "description": "Lists all S3 buckets in your account"
    },
    "List EC2 Instances": {
        "command": "ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name,InstanceType]' --output table",
        "description": "Lists EC2 instances with their state and type"
    },
    "Get Account Info": {
        "command": "sts get-caller-identity",
        "description": "Shows current AWS account and user information"
    },
    "List IAM Users": {
        "command": "iam list-users --query 'Users[*].[UserName,CreateDate]' --output table",
        "description": "Lists IAM users with creation dates"
    },
    "List Lambda Functions": {
        "command": "lambda list-functions --query 'Functions[*].[FunctionName,Runtime,LastModified]' --output table",
        "description": "Lists Lambda functions with runtime info"
    },
    "List RDS Instances": {
        "command": "rds describe-db-instances --query 'DBInstances[*].[DBInstanceIdentifier,Engine,DBInstanceStatus]' --output table",
        "description": "Lists RDS database instances"
    },
    "List VPCs": {
        "command": "ec2 describe-vpcs --query 'Vpcs[*].[VpcId,CidrBlock,State]' --output table",
        "description": "Lists VPCs with their CIDR blocks"
    },
    "Get Cost Explorer": {
        "command": "ce get-cost-and-usage --time-period Start=2024-01-01,End=2024-01-31 --granularity MONTHLY --metrics 'UnblendedCost'",
        "description": "Gets cost data for specified period"
    }
}

# Example of blocked dangerous operations
DANGEROUS_EXAMPLES = {
    "Delete S3 Bucket": {
        "command": "s3api delete-bucket --bucket my-bucket",
        "description": "❌ BLOCKED: Deletes an S3 bucket"
    },
    "Terminate EC2 Instance": {
        "command": "ec2 terminate-instances --instance-ids i-1234567890abcdef0",
        "description": "❌ BLOCKED: Terminates EC2 instances"
    },
    "Delete IAM User": {
        "command": "iam delete-user --user-name my-user",
        "description": "❌ BLOCKED: Deletes IAM user"
    }
}

def print_examples():
    """Print example AWS CLI commands"""
    print("\n" + "="*60)
    print("AWS CLI MCP Server - Example Commands")
    print("="*60)
    
    print("\n✅ SAFE OPERATIONS (These will work):")
    print("-"*60)
    for name, info in SAFE_EXAMPLES.items():
        print(f"\n{name}:")
        print(f"  Command: aws {info['command']}")
        print(f"  Description: {info['description']}")
    
    print("\n\n❌ DANGEROUS OPERATIONS (These are blocked for safety):")
    print("-"*60)
    for name, info in DANGEROUS_EXAMPLES.items():
        print(f"\n{name}:")
        print(f"  Command: aws {info['command']}")
        print(f"  Description: {info['description']}")
    
    print("\n" + "="*60)
    print("\n💡 Tips:")
    print("  - The MCP server automatically adds --output json if not specified")
    print("  - Use --query to filter results")
    print("  - Use --output table for human-readable output")
    print("  - Dangerous commands (delete/terminate) are blocked by default")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    print_examples()
    
    # Check if AWS credentials are configured
    if not os.environ.get("AWS_ACCESS_KEY_ID"):
        print("⚠️  Warning: AWS_ACCESS_KEY_ID not found in environment")
        print("   Make sure to configure your AWS credentials!")
