import asyncio
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from difflib import SequenceMatcher
import re
class MCPClient:
    """Client for communicating with MCP servers."""
    
    def __init__(self):
        self.servers: Dict[str, MCPServer] = {}
        self.request_counter = 0
    
    def register_server(self, server: MCPServer):
        """Register an MCP server."""
        self.servers[server.name] = server
        print(f"[MCPClient] Registered server: {server.name}")
    
    async def call_tool(self, server_name: str, tool_name: str, **kwargs) -> Any:
        """Call a tool on a specific MCP server."""
        if server_name not in self.servers:
            raise ValueError(f"Server {server_name} not found")
        
        self.request_counter += 1
        request = MCPRequest(
            method="tools/call",
            params={"name": tool_name, "arguments": kwargs},
            id=f"req-{self.request_counter}"
        )
        
        response = await self.servers[server_name].handle_request(request)
        
        if response.error:
            raise Exception(f"MCP Error: {response.error}")
        
        return response.result
    
    async def list_tools(self, server_name: str) -> List[str]:
        """List available tools on a server."""
        if server_name not in self.servers:
            raise ValueError(f"Server {server_name} not found")
        
        request = MCPRequest(
            method="tools/list",
            params={},
            id=f"req-list-{self.request_counter}"
        )
        
        response = await self.servers[server_name].handle_request(request)
        return response.result.get("tools", [])
