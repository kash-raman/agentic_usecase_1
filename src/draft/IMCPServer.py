import asyncio
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from difflib import SequenceMatcher
import re
class MCPServer(ABC):
    """Base class for MCP servers implementing Model Context Protocol."""
    
    def __init__(self, name: str, data_hub: DataHub):
        self.name = name
        self.data_hub = data_hub
        self.tools: Dict[str, Callable] = {}
        self.resources: Dict[str, Any] = {}
        self._register_tools()
    
    @abstractmethod
    def _register_tools(self):
        """Register available tools/capabilities."""
        pass
    
    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle incoming MCP request."""
        try:
            self.log(f"Received request: {request.method}")
            
            if request.method == "tools/list":
                return MCPResponse(
                    result={"tools": list(self.tools.keys())},
                    id=request.id
                )
            
            elif request.method == "tools/call":
                tool_name = request.params.get("name")
                tool_params = request.params.get("arguments", {})
                
                if tool_name not in self.tools:
                    return MCPResponse(
                        error=f"Tool {tool_name} not found",
                        id=request.id
                    )
                
                result = await self.tools[tool_name](**tool_params)
                return MCPResponse(result=result, id=request.id)
            
            elif request.method == "resources/list":
                return MCPResponse(
                    result={"resources": list(self.resources.keys())},
                    id=request.id
                )
            
            else:
                return MCPResponse(
                    error=f"Unknown method: {request.method}",
                    id=request.id
                )
        
        except Exception as e:
            self.log(f"Error handling request: {e}")
            return MCPResponse(error=str(e), id=request.id)
    
    def register_tool(self, name: str, func: Callable):
        """Register a tool capability."""
        self.tools[name] = func
        self.log(f"Registered tool: {name}")
    
    def log(self, message: str):
        """Log server activity."""
        print(f"[{self.name}] {message}")

