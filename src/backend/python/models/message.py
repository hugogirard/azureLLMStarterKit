from pydantic import BaseModel, Field

class Message(BaseModel):
    id: str  
    prompt: str
    type: str = 'Message'
    session_id:str = Field(default=None, alias='sessionId')
    user_name: str = Field(default=None, alias='username')
    completion: str