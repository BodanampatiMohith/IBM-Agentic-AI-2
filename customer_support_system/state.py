from __future__ import annotations

from typing import Annotated, Any, Dict, List, Optional, TypedDict


class SupportState(TypedDict, total=False):
    customer_id: str
    customer_name: str
    query: str
    intent: str
    department: str
    retrieved_context: List[Dict[str, Any]]
    draft_response: str
    final_response: str
    approval_required: bool
    approval_status: str
    approved: bool
    memory_recall: Optional[str]
    history: List[Dict[str, Any]]
    supervisor_feedback: Optional[str]
