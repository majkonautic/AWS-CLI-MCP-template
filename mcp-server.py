#!/usr/bin/env python3
"""AWS CLI MCP Server - Allows Claude to execute AWS CLI commands."""

import asyncio
import json
import subprocess
import sys
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Resource

# List of potentially dangerous AWS CLI commands that should be blocked
DANGEROUS_COMMANDS = [
    "delete",
    "terminate",
    "destroy",
    "remove",
    "rm",
    "purge",
    "deregister",
    "disassociate",
    "detach",
]

def is_dangerous_command(command: str) -> bool:
    """Check if a command contains dangerous operations."""
    command_lower = command.lower()
    return any(dangerous in command_lower for dangerous in DANGEROUS_COMMANDS)

async def run_aws_command(command: str, region: Optional[str] = None, profile: Optional[str] = None) -> str:
    """Execute an AWS CLI command and return the output."""
    cmd_parts = ["aws"] + command.split()
    
    if region:
        cmd_parts.extend(["--region", region])
    
    if profile:
        cmd_parts.extend(["--profile", profile])
    
    # Add JSON output if not specified
    if "--output" not in command:
        cmd_parts.extend(["--output", "json"])
    
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd_parts,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_msg = stderr.decode().strip()
            return f"Error: {error_msg}"
        
        return stdout.decode().strip()
    except Exception as e:
        return f"Error executing command: {str(e)}"

# Create the MCP server
server = Server("aws-cli-mcp")

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available AWS CLI tools."""
    return [
        Tool(
            name="aws_cli",
            description="Execute AWS CLI commands. Dangerous operations like delete/terminate are blocked.",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "AWS CLI command to execute (without 'aws' prefix). Example: 's3 ls'"
                    },
                    "region": {
                        "type": "string",
                        "description": "AWS region (optional, uses default if not specified)"
                    },
                    "profile": {
                        "type": "string",
                        "description": "AWS profile to use (optional, uses default if not specified)"
                    }
                },
                "required": ["command"]
            }
        ),
        Tool(
            name="list_profiles",
            description="List available AWS profiles configured on the system",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_caller_identity",
            description="Get details about the current AWS credentials",
            inputSchema={
                "type": "object",
                "properties": {
                    "profile": {
                        "type": "string",
                        "description": "AWS profile to use (optional)"
                    }
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Execute AWS CLI tools."""
    
    if name == "aws_cli":
        command = arguments.get("command", "")
        
        # Safety check
        if is_dangerous_command(command):
            return [TextContent(
                type="text",
                text="❌ Dangerous command blocked. Commands containing delete/terminate/destroy operations are not allowed for safety."
            )]
        
        region = arguments.get("region")
        profile = arguments.get("profile")
        
        result = await run_aws_command(command, region, profile)
        
        return [TextContent(
            type="text",
            text=result
        )]
    
    elif name == "list_profiles":
        try:
            process = await asyncio.create_subprocess_exec(
                "aws", "configure", "list-profiles",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                return [TextContent(
                    type="text",
                    text=f"Error listing profiles: {stderr.decode().strip()}"
                )]
            
            profiles = stdout.decode().strip()
            return [TextContent(
                type="text",
                text=f"Available AWS profiles:\n{profiles}" if profiles else "No AWS profiles configured"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )]
    
    elif name == "get_caller_identity":
        profile = arguments.get("profile")
        result = await run_aws_command("sts get-caller-identity", profile=profile)
        
        return [TextContent(
            type="text",
            text=result
        )]
    
    return [TextContent(
        type="text",
        text=f"Unknown tool: {name}"
    )]

@server.list_resources()
async def list_resources() -> List[Resource]:
    """List available resources."""
    return []

async def main():
    """Run the AWS CLI MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
