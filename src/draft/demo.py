import asyncio
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from difflib import SequenceMatcher
import re
async def demo():
    """Demonstrate the MCP-based document verification system."""
    
    # Sample documents
    bank_statement = """
    BANK OF EXAMPLE
    Monthly Statement
    
    Name: John Michael Smith
    Address: 123 Main Street
    Apartment 4B
    New York, NY 10001
    
    Account Number: 1234567890
    Statement Period: October 2025
    """
    
    credit_report = """
    CREDIT BUREAU REPORT
    
    Consumer Name: John M. Smith
    Current Address: 123 Main St, Apt 4B
    New York, NY 10001
    
    SSN: XXX-XX-1234
    Date of Birth: 01/15/1985
    """
    
    # Initialize system
    system = DocumentVerificationSystem()
    
    # Show MCP server capabilities
    print("\n" + "="*80)
    print("MCP SERVER CAPABILITIES")
    print("="*80)
    capabilities = await system.get_server_capabilities()
    for server, tools in capabilities.items():
        print(f"\n{server}:")
        for tool in tools:
            print(f"  - {tool}")
    print("="*80 + "\n")
    
    # Process documents
    decision = await system.process_documents(
        request_id="REQ-2025-001",
        bank_statement=bank_statement,
        credit_report=credit_report
    )
    
    # Get full report
    report = await system.get_full_report("REQ-2025-001")
    
    print("\n" + "="*80)
    print("FULL VERIFICATION REPORT")
    print("="*80)
    print(json.dumps(report, indent=2, default=str))
    print("="*80 + "\n")


if __name__ == "__main__":
    # Run demo
    asyncio.run(demo())