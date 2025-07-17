FROM python:3.11-slim

# Install AWS CLI v2
RUN apt-get update && \
    apt-get install -y curl unzip && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
RUN pip install mcp

# Copy the MCP server
COPY mcp-server.py .
RUN chmod +x mcp-server.py

# Create directory for AWS credentials
RUN mkdir -p /root/.aws

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the MCP server
CMD ["python3", "mcp-server.py"]
