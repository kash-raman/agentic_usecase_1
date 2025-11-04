import asyncio
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from difflib import SequenceMatcher
import re

class DocumentType(Enum):
    BANK_STATEMENT = "bank_statement"
    CREDIT_REPORT = "credit_report"


class VerificationStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class MatchResult(Enum):
    EXACT_MATCH = "exact_match"
    PARTIAL_MATCH = "partial_match"
    MISMATCH = "mismatch"


@dataclass
class CustomerInfo:
    name: str
    address: str
    document_type: DocumentType
    extracted_at: str
    confidence_score: float = 1.0
    metadata: Dict[str, Any] = None

    def to_dict(self):
        result = asdict(self)
        result['document_type'] = self.document_type.value
        return result


@dataclass
class VerificationResult:
    request_id: str
    name_match: MatchResult
    address_match: MatchResult
    overall_match: bool
    confidence_score: float
    details: Dict[str, Any]
    timestamp: str


@dataclass
class SupervisorDecision:
    request_id: str
    approved: bool
    action: str
    reason: str
    timestamp: str


@dataclass
class MCPRequest:
    """Request structure for MCP protocol."""
    method: str
    params: Dict[str, Any]
    id: str


@dataclass
class MCPResponse:
    """Response structure for MCP protocol."""
    result: Any
    error: Optional[str] = None
    id: Optional[str] = None

