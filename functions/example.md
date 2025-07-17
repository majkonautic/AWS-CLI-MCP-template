# AWS CLI MCP Functions Example

This directory can contain example AWS scripts or CloudFormation templates that work with the MCP server.

## Example: Create S3 Bucket with Versioning

\`\`\`bash
# Create bucket
aws s3api create-bucket --bucket my-example-bucket --region us-east-1

# Enable versioning
aws s3api put-bucket-versioning \
    --bucket my-example-bucket \
    --versioning-configuration Status=Enabled

# Add lifecycle policy
aws s3api put-bucket-lifecycle-configuration \
    --bucket my-example-bucket \
    --lifecycle-configuration file://lifecycle.json
\`\`\`

## Example: List EC2 Instances by Tag

\`\`\`bash
aws ec2 describe-instances \
    --filters "Name=tag:Environment,Values=Production" \
    --query 'Reservations[*].Instances[*].[InstanceId,Tags[?Key==\`Name\`]|[0].Value,State.Name]' \
    --output table
\`\`\`

## Example: Get AWS Cost Report

\`\`\`bash
aws ce get-cost-and-usage \
    --time-period Start=2024-01-01,End=2024-01-31 \
    --granularity MONTHLY \
    --metrics "BlendedCost" \
    --group-by Type=DIMENSION,Key=SERVICE \
    --output table
\`\`\`

## Example: List Lambda Functions by Runtime

\`\`\`bash
aws lambda list-functions \
    --query 'Functions[?Runtime==\`python3.11\`].[FunctionName,CodeSize,LastModified]' \
    --output table
\`\`\`
