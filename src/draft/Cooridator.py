import asyncio
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from difflib import SequenceMatcher
import re

class CoordinatorMCPServer(MCPServer):
    """MCP Server for coordinating verification process."""
    
    def __init__(self, data_hub: DataHub):
        super().__init__("CoordinatorMCPServer", data_hub)
    
    def _register_tools(self):
        """Register coordination tools."""
        self.register_tool("verify_documents", self.verify_documents)
        self.register_tool("compare_fields", self.compare_fields)
        self.register_tool("calculate_similarity", self.calculate_similarity)
    
    async def verify_documents(self, request_id: str) -> Dict[str, Any]:
        """Compare customer information from both documents."""
        self.log(f"Verifying data for request {request_id}")
        
        # Wait for data to be complete
        while not await self.data_hub.is_data_complete(request_id):
            await asyncio.sleep(0.5)
        
        # Retrieve data from Data Hub
        customer_data = await self.data_hub.get_customer_info(request_id)
        
        bank_info = customer_data[DocumentType.BANK_STATEMENT]
        credit_info = customer_data[DocumentType.CREDIT_REPORT]
        
        # Compare names
        name_match = self._compare_names(bank_info.name, credit_info.name)
        name_similarity = self._calculate_similarity(bank_info.name, credit_info.name)
        
        # Compare addresses
        address_match = self._compare_addresses(bank_info.address, credit_info.address)
        address_similarity = self._calculate_similarity(bank_info.address, credit_info.address)
        
        # Calculate overall confidence
        confidence_score = (name_similarity + address_similarity) / 2
        overall_match = name_match != MatchResult.MISMATCH and address_match != MatchResult.MISMATCH
        
        result = VerificationResult(
            request_id=request_id,
            name_match=name_match,
            address_match=address_match,
            overall_match=overall_match,
            confidence_score=confidence_score,
            details={
                "bank_statement": bank_info.to_dict(),
                "credit_report": credit_info.to_dict(),
                "name_similarity": name_similarity,
                "address_similarity": address_similarity
            },
            timestamp=datetime.now().isoformat()
        )
        
        # Store result in Data Hub
        await self.data_hub.store_verification_result(result)
        
        self.log(f"Verification completed: {name_match.value}, {address_match.value}")
        return asdict(result)
    
    async def compare_fields(self, field1: str, field2: str, field_type: str) -> Dict[str, Any]:
        """Compare two fields and return similarity metrics."""
        similarity = self._calculate_similarity(field1, field2)
        
        if field_type == "name":
            match = self._compare_names(field1, field2)
        else:
            match = self._compare_addresses(field1, field2)
        
        return {
            "similarity": similarity,
            "match_result": match.value,
            "field_type": field_type
        }
    
    async def calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity ratio between two strings."""
        return self._calculate_similarity(str1, str2)
    
    def _compare_names(self, name1: str, name2: str) -> MatchResult:
        """Compare two names and return match result."""
        similarity = self._calculate_similarity(name1, name2)
        
        if similarity >= 0.95:
            return MatchResult.EXACT_MATCH
        elif similarity >= 0.75:
            return MatchResult.PARTIAL_MATCH
        else:
            return MatchResult.MISMATCH
    
    def _compare_addresses(self, addr1: str, addr2: str) -> MatchResult:
        """Compare two addresses and return match result."""
        similarity = self._calculate_similarity(addr1, addr2)
        
        if similarity >= 0.90:
            return MatchResult.EXACT_MATCH
        elif similarity >= 0.70:
            return MatchResult.PARTIAL_MATCH
        else:
            return MatchResult.MISMATCH
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity ratio between two strings."""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
