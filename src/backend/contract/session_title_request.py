
from pydantic import BaseModel, Field


class SessionTitleRequest(BaseModel):
    session_id:str = Field(alias="sessionId")
    prompt: str    