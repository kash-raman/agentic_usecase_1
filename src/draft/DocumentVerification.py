
# ============================================================================
# ORCHESTRATION SYSTEM
# ============================================================================
import asyncio
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from difflib import SequenceMatcher
import re
class DocumentVerificationSystem:
    """Main orchestration system using MCP servers."""
    
    def __init__(self):
        self.data_hub = DataHub()
        self.mcp_client = MCPClient()
        
        # Initialize MCP servers
        self.bank_server = BankStatementMCPServer(self.data_hub)
        self.credit_server = CreditReportMCPServer(self.data_hub)
        self.coordinator_server = CoordinatorMCPServer(self.data_hub)
        self.supervisor_server = SupervisorMCPServer(self.data_hub)
        
        # Register servers with client
        self.mcp_client.register_server(self.bank_server)
        self.mcp_client.register_server(self.credit_server)
        self.mcp_client.register_server(self.coordinator_server)
        self.mcp_client.register_server(self.supervisor_server)
    
    async def process_documents(self, request_id: str, 
                               bank_statement: str, 
                               credit_report: str) -> SupervisorDecision:
        """Process documents through the MCP-based verification pipeline."""
        
        print(f"\n{'='*80}")
        print(f"Starting MCP-based verification for request: {request_id}")
        print(f"{'='*80}\n")
        
        # Call extraction tools in parallel via MCP
        extraction_tasks = [
            self.mcp_client.call_tool(
                "BankStatementMCPServer",
                "extract_customer_info",
                request_id=request_id,
                document_content=bank_statement
            ),
            self.mcp_client.call_tool(
                "CreditReportMCPServer",
                "extract_customer_info",
                request_id=request_id,
                document_content=credit_report
            )
        ]
        
        await asyncio.gather(*extraction_tasks)
        
        # Call coordinator for verification
        verification_result = await self.mcp_client.call_tool(
            "CoordinatorMCPServer",
            "verify_documents",
            request_id=request_id
        )
        
        print(f"\n[System] Verification complete: confidence={verification_result['confidence_score']:.2%}")
        
        # Call supervisor for decision
        decision_dict = await self.mcp_client.call_tool(
            "SupervisorMCPServer",
            "make_decision",
            request_id=request_id
        )
        
        decision = SupervisorDecision(**decision_dict)
        
        print(f"\n{'='*80}")
        print(f"Verification completed for request: {request_id}")
        print(f"Decision: {decision.action}")
        print(f"Reason: {decision.reason}")
        print(f"{'='*80}\n")
        
        return decision
    
    async def get_server_capabilities(self) -> Dict[str, List[str]]:
        """Get capabilities of all MCP servers."""
        capabilities = {}
        
        for server_name in self.mcp_client.servers.keys():
            tools = await self.mcp_client.list_tools(server_name)
            capabilities[server_name] = tools
        
        return capabilities
    
    async def get_full_report(self, request_id: str) -> Dict[str, Any]:
        """Get complete report for a request."""
        customer_data = await self.data_hub.get_customer_info(request_id)
        verification_result = await self.data_hub.get_verification_result(request_id)
        supervisor_decision = await self.data_hub.get_supervisor_decision(request_id)
        
        return {
            "request_id": request_id,
            "customer_data": {k.value: v.to_dict() for k, v in customer_data.items()},
            "verification": asdict(verification_result) if verification_result else None,
            "decision": asdict(supervisor_decision) if supervisor_decision else None
        }
