from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class Conversations(BaseModel):
    session_id: str
    message_id: int
    user_query: str
    response: str
    is_interrupt: bool
    llm_model: str
    tool_used: Optional[Any] = None
    token_count: Optional[dict[Any, Any]] = None
    current_token_count: Optional[int] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    
class IntervisionObject(BaseModel):
    content: Optional[str] = None 
    allowed_actions: Optional[list] = None
    action_name: Optional[str] = None
    