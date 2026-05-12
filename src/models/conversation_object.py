from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class Conversations(BaseModel):
    user_query: str
    response: str
    llm_model: str
    tool_used: Optional[list[str]] = None
    token_count: Optional[dict[str, int]] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None