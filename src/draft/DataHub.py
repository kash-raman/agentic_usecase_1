import asyncio
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from difflib import SequenceMatcher
import re
class DataHub:
    """Centralized repository for storing and retrieving extracted document data."""
    
    def __init__(self):
        self._data: Dict[str, Dict[DocumentType, CustomerInfo]] = {}
        self._verification_results: Dict[str, VerificationResult] = {}
        self._supervisor_decisions: Dict[str, SupervisorDecision] = {}
        self._lock = asyncio.Lock()
        self._event_subscribers: Dict[str, List[Callable]] = {}
    
    async def store_customer_info(self, request_id: str, info: CustomerInfo):
        """Store extracted customer information."""
        async with self._lock:
            if request_id not in self._data:
                self._data[request_id] = {}
            self._data[request_id][info.document_type] = info
            print(f"[DataHub] Stored {info.document_type.value} data for request {request_id}")
            
            # Notify subscribers
            await self._notify_subscribers(f"data_stored_{request_id}", info)
    
    async def get_customer_info(self, request_id: str) -> Dict[DocumentType, CustomerInfo]:
        """Retrieve all customer information for a request."""
        async with self._lock:
            return self._data.get(request_id, {})
    
    async def is_data_complete(self, request_id: str) -> bool:
        """Check if data from both documents is available."""
        async with self._lock:
            data = self._data.get(request_id, {})
            return (DocumentType.BANK_STATEMENT in data and 
                    DocumentType.CREDIT_REPORT in data)
    
    async def store_verification_result(self, result: VerificationResult):
        """Store verification result."""
        async with self._lock:
            self._verification_results[result.request_id] = result
            print(f"[DataHub] Stored verification result for request {result.request_id}")
            await self._notify_subscribers(f"verification_complete_{result.request_id}", result)
    
    async def get_verification_result(self, request_id: str) -> Optional[VerificationResult]:
        """Retrieve verification result."""
        async with self._lock:
            return self._verification_results.get(request_id)
    
    async def store_supervisor_decision(self, decision: SupervisorDecision):
        """Store supervisor decision."""
        async with self._lock:
            self._supervisor_decisions[decision.request_id] = decision
            print(f"[DataHub] Stored supervisor decision for request {decision.request_id}")
    
    async def get_supervisor_decision(self, request_id: str) -> Optional[SupervisorDecision]:
        """Retrieve supervisor decision."""
        async with self._lock:
            return self._supervisor_decisions.get(request_id)
    
    def subscribe(self, event: str, callback: Callable):
        """Subscribe to data hub events."""
        if event not in self._event_subscribers:
            self._event_subscribers[event] = []
        self._event_subscribers[event].append(callback)
    
    async def _notify_subscribers(self, event: str, data: Any):
        """Notify subscribers of an event."""
        if event in self._event_subscribers:
            for callback in self._event_subscribers[event]:
                try:
                    await callback(data)
                except Exception as e:
                    print(f"[DataHub] Error notifying subscriber: {e}")
