from typing import TypedDict, Annotated, Literal
import operator
from langchain_core.messages import BaseMessage

class SupportState(TypedDict):
    """Sistem durumu için state sınıfı"""
    messages: Annotated[list[BaseMessage], operator.add]
    customer_id: str
    issue_category: str
    priority: str
    sentiment: str
    resolution_status: str
    ticket_id: str
    requires_human: bool
    context: dict