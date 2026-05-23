from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class Conversations(BaseModel):
    user_query: str
    response: str
    is_interrupt: bool
    llm_model: str
    tool_used: Optional[Any] = None
    token_count: Optional[dict[str, Any]] = None
    current_token_count: Optional[int] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    
class IntervisionObject(BaseModel):
    content: Optional[str] = None 
    allowed_actions: Optional[list] = None
    action_name: Optional[str] = None
    