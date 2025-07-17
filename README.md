# AWS CLI MCP Template

This lets Claude control your AWS CLI commands safely!

## 🚀 Quick Start

### 1. Clone it to your project folder

\`\`\`bash
git clone https://github.com/majkonautic/AWS-CLI-MCP-template.git aws-cli-mcp
cd aws-cli-mcp
\`\`\`

### 2. Add your AWS credentials

\`\`\`bash
cp .env.example .env
\`\`\`

Now edit \`.env\` and add your real AWS credentials:
\`\`\`
AWS_ACCESS_KEY_ID=your-actual-access-key
AWS_SECRET_ACCESS_KEY=your-actual-secret-key
AWS_DEFAULT_REGION=us-east-1
\`\`\`

### 3. Run the setup

\`\`\`bash
./setup.sh
\`\`\`

### 4. Go back to your project root and connect to Claude

\`\`\`bash
cd ..
claude mcp add aws-local python3 aws-cli-mcp/mcp-server.py
\`\`\`

That's it! Now Claude can execute AWS CLI commands!

## 🛡️ Safety Features

This MCP server blocks dangerous commands by default:
- ❌ delete
- ❌ terminate
- ❌ destroy
- ❌ remove
- ❌ purge

Only read and list operations are allowed for safety.

## 📋 Available Tools

1. **aws_cli** - Execute any safe AWS CLI command
2. **list_profiles** - List configured AWS profiles
3. **get_caller_identity** - Get current AWS credentials info

## 📖 Example Commands

### Safe Operations (These work):
- \`aws s3 ls\` - List S3 buckets
- \`aws ec2 describe-instances\` - List EC2 instances
- \`aws lambda list-functions\` - List Lambda functions
- \`aws iam list-users\` - List IAM users

### Blocked Operations (For safety):
- \`aws s3 rm\` - ❌ Blocked
- \`aws ec2 terminate-instances\` - ❌ Blocked
- \`aws iam delete-user\` - ❌ Blocked

## 🐳 Docker Support

Build and run with Docker:

\`\`\`bash
docker build -t aws-cli-mcp .
docker run -v ~/.aws:/root/.aws:ro aws-cli-mcp
\`\`\`

## 📝 License

MIT License - see LICENSE file for details.
