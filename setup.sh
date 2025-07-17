#!/bin/bash

echo "🚀 Setting up AWS CLI MCP Server..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed. Please install AWS CLI v2."
    echo "   Visit: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install MCP package
echo "📦 Installing MCP SDK..."
pip install mcp

# Check AWS configuration
echo "🔍 Checking AWS configuration..."
if aws configure list-profiles | grep -q .; then
    echo "✅ AWS profiles found:"
    aws configure list-profiles
else
    echo "⚠️  No AWS profiles configured. Run 'aws configure' to set up your credentials."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use with Claude Code, run:"
echo "  claude mcp add aws-local python3 $(pwd)/mcp-server.py"
echo ""
echo "Make sure to configure your AWS credentials if you haven't already:"
echo "  aws configure"
echo ""

# Make the script executable
chmod +x mcp-server.py
