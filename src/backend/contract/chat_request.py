from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    session_id:str = Field(alias="sessionId")
    question: str
