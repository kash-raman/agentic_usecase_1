import asyncio
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from difflib import SequenceMatcher
import re

class SupervisorMCPServer(MCPServer):
    """MCP Server for supervisor decision-making."""
    
    def __init__(self, data_hub: DataHub):
        super().__init__("SupervisorMCPServer", data_hub)
    
    def _register_tools(self):
        """Register supervisor tools."""
        self.register_tool("make_decision", self.make_decision)
        self.register_tool("review_case", self.review_case)
        self.register_tool("escalate_case", self.escalate_case)
    
    async def make_decision(self, request_id: str) -> Dict[str, Any]:
        """Make decision based on verification result."""
        self.log(f"Reviewing verification result for request {request_id}")
        
        # Retrieve verification result
        result = await self.data_hub.get_verification_result(request_id)
        
        if not result:
            raise ValueError(f"No verification result found for request {request_id}")
        
        # Decision logic
        decision = self._make_decision(result)
        
        # Store decision
        await self.data_hub.store_supervisor_decision(decision)
        
        self.log(f"Decision: {decision.action} - {decision.reason}")
        return asdict(decision)
    
    async def review_case(self, request_id: str) -> Dict[str, Any]:
        """Perform detailed review of a case."""
        result = await self.data_hub.get_verification_result(request_id)
        
        return {
            "request_id": request_id,
            "review_status": "completed",
            "confidence": result.confidence_score if result else 0,
            "recommendation": "Requires additional documentation" if result and result.confidence_score < 0.8 else "Approve"
        }
    
    async def escalate_case(self, request_id: str, reason: str) -> Dict[str, Any]:
        """Escalate case to human supervisor."""
        self.log(f"Escalating case {request_id}: {reason}")
        return {
            "request_id": request_id,
            "escalated": True,
            "reason": reason,
            "escalated_at": datetime.now().isoformat()
        }
    
    def _make_decision(self, result: VerificationResult) -> SupervisorDecision:
        """Determine action based on verification result."""
        
        # Exact match on both fields
        if (result.name_match == MatchResult.EXACT_MATCH and 
            result.address_match == MatchResult.EXACT_MATCH):
            return SupervisorDecision(
                request_id=result.request_id,
                approved=True,
                action="AUTO_APPROVE",
                reason="All fields match exactly",
                timestamp=datetime.now().isoformat()
            )
        
        # Mismatch on critical field (name)
        if result.name_match == MatchResult.MISMATCH:
            return SupervisorDecision(
                request_id=result.request_id,
                approved=False,
                action="REJECT",
                reason="Name mismatch detected",
                timestamp=datetime.now().isoformat()
            )
        
        # Partial matches or address mismatch
        if (result.name_match == MatchResult.PARTIAL_MATCH or 
            result.address_match != MatchResult.EXACT_MATCH):
            return SupervisorDecision(
                request_id=result.request_id,
                approved=False,
                action="MANUAL_REVIEW",
                reason=f"Partial match detected (confidence: {result.confidence_score:.2%})",
                timestamp=datetime.now().isoformat()
            )
        
        # Default to manual review
        return SupervisorDecision(
            request_id=result.request_id,
            approved=False,
            action="MANUAL_REVIEW",
            reason="Unable to determine automatically",
            timestamp=datetime.now().isoformat()
        )
