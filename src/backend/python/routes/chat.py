from typing import Annotated
from fastapi import HTTPException
from services.chat_service import ChatService
from dependencies import get_chat_service, get_logger, get_easy_auth_token
from models import Message
from contract import ChatRequest
from logging import Logger
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/chat"
)

@router.post('/')
async def chat(chat_request: ChatRequest, 
               user_principal_name: Annotated[str, Depends(get_easy_auth_token)], 
               logger: Annotated[Logger, Depends(get_logger)],
               chat: Annotated[ChatService, Depends(get_chat_service)]) -> Message:
    try:
        return await chat.completion(chat_request, user_principal_name)
    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=500, detail='Internal Server Error')


