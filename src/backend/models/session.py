from typing import Optional
from pydantic import BaseModel, Field

class Session(BaseModel):
    id: str
    title: str
    session_id: str = Field(default=None, alias='sessionId')
    type:str = 'Session'
    user_name: str = Field(default=None, alias='username')
