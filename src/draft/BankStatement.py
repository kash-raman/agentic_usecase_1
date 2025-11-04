import asyncio
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from difflib import SequenceMatcher
import re

class BankStatementMCPServer(MCPServer):
    """MCP Server for bank statement processing."""
    
    def __init__(self, data_hub: DataHub):
        super().__init__("BankStatementMCPServer", data_hub)
    
    def _register_tools(self):
        """Register bank statement processing tools."""
        self.register_tool("extract_customer_info", self.extract_customer_info)
        self.register_tool("validate_document", self.validate_document)
    
    async def extract_customer_info(self, request_id: str, document_content: str) -> Dict[str, Any]:
        """Extract customer information from bank statement."""
        self.log(f"Processing bank statement for request {request_id}")
        
        # Simulate processing time
        await asyncio.sleep(1)
        
        # Extract name and address
        name = self._extract_name(document_content)
        address = self._extract_address(document_content)
        
        customer_info = CustomerInfo(
            name=name,
            address=address,
            document_type=DocumentType.BANK_STATEMENT,
            extracted_at=datetime.now().isoformat(),
            confidence_score=0.95,
            metadata={"source": "bank_statement_parser", "mcp_server": self.name}
        )
        
        # Store in Data Hub
        await self.data_hub.store_customer_info(request_id, customer_info)
        self.log(f"Extracted and stored bank statement data for {name}")
        
        return customer_info.to_dict()
    
    async def validate_document(self, document_content: str) -> Dict[str, Any]:
        """Validate bank statement format and content."""
        # Simplified validation logic
        is_valid = "BANK" in document_content and "Name:" in document_content
        return {
            "valid": is_valid,
            "confidence": 0.9 if is_valid else 0.3,
            "issues": [] if is_valid else ["Missing required fields"]
        }
    
    def _extract_name(self, content: str) -> str:
        """Extract customer name from document content."""
        match = re.search(r"Name:\s*(.+?)(?:\n|$)", content)
        return match.group(1).strip() if match else "Unknown"
    
    def _extract_address(self, content: str) -> str:
        """Extract customer address from document content."""
        match = re.search(r"Address:\s*(.+?)(?:\n\n|Account)", content, re.DOTALL)
        return match.group(1).strip().replace("\n", ", ") if match else "Unknown"
