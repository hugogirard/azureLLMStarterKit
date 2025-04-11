from fastapi import APIRouter, Depends, HTTPException, Header
from dependencies import get_chat_service, get_session_repository, get_easy_auth_token, get_logger
from repository.session_repository import SessionRepository
from logging import Logger
from models import Session, Message
from typing import Annotated, List
from contract import SessionTitleRequest
import uuid

from services.kernel_chat_service import KernelChatService

router = APIRouter(prefix="/session")

@router.post('/new')
async def new_session(logger: Annotated[Logger, Depends(get_logger)],
                      session_repository: Annotated[SessionRepository, Depends(get_session_repository)],
                      user_principal_name: Annotated[str, Depends(get_easy_auth_token)]) -> Session:
    try:
        
        id = str(uuid.uuid4())
        session = Session(id=id,title=id)
        session.session_id = id              
        session.user_name = user_principal_name   
        await session_repository.create_new_session(session)
        return session   
         
    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=500, detail='Internal Server Error')        

@router.post('/newtitle')
async def new_title(session_title_request:SessionTitleRequest,
                    user_principal_name: Annotated[str, Depends(get_easy_auth_token)],
                    chat: Annotated[KernelChatService, Depends(get_chat_service)],
                    logger: Annotated[Logger, Depends(get_logger)],
                    session_repository: Annotated[SessionRepository, Depends(get_session_repository)]) -> str:
   
   session = await session_repository.get_session(session_title_request.session_id,
                                                  user_principal_name)
   
   title = await chat.summarize(session_title_request.prompt)

   session.title = title

   await session_repository.update_session(Session(id=session.id,
                                                   title=title,
                                                   session_id=session.session_id,
                                                   username=user_principal_name))

   return str

@router.get('/all')
async def get_session(user_principal_name: Annotated[str, Depends(get_easy_auth_token)],
                      logger: Annotated[Logger, Depends(get_logger)],
                      session_repository: Annotated[SessionRepository, Depends(get_session_repository)]) -> List[Session]:
    try:
      
      sessions = await session_repository.get_all_sessions(user_principal_name)
      return sessions
    
    except Exception as err:
      logger.error(err)
      raise HTTPException(status_code=500, detail='Internal Server Error')         

# get a specific session by session id
@router.get("/{sessionId}")
async def get_session_by_id(sessionId: str, 
                            user_principal_name: Annotated[str, Depends(get_easy_auth_token)],                            
                            logger: Annotated[Logger, Depends(get_logger)],
                            session_repository: Annotated[SessionRepository, Depends(get_session_repository)]) -> Session:
    try:      
      session = await session_repository.get_session(session_id=sessionId,username=user_principal_name)
      if not session:
         raise HTTPException(status_code=404, detail="Session not found")
      return session

    except Exception as err:
      logger.error(err)
      raise HTTPException(status_code=500, detail='Internal Server Error')            


@router.get('/{sessionid}/messages')
async def get_message_session(sessionid: str,
                              user_principal_name: Annotated[str, Depends(get_easy_auth_token)],      
                              logger: Annotated[Logger, Depends(get_logger)],
                              session_repository: Annotated[SessionRepository, Depends(get_session_repository)]) -> List[Message]:
    try:
      return await session_repository.get_session_messages(session_id=sessionid, username=user_principal_name)
    except Exception as err:
      logger.error(err)
      raise HTTPException(status_code=500, detail='Internal Server Error')          

@router.delete('/{sessionid}')
async def delete_session(sessionid: str, 
                         user_principal_name: Annotated[str, Depends(get_easy_auth_token)],      
                         logger: Annotated[Logger, Depends(get_logger)],
                         session_repository: Annotated[SessionRepository, Depends(get_session_repository)]):

    try:      
      await session_repository.delete_session(session_id=sessionid,username=user_principal_name)      
    except Exception as err:
      logger.error(err)
      raise HTTPException(status_code=500, detail='Internal Server Error')        


@router.delete('/all/')
async def delete_session(user_principal_name: Annotated[str, Depends(get_easy_auth_token)], 
                         logger: Annotated[Logger, Depends(get_logger)],
                         session_repository: Annotated[SessionRepository, Depends(get_session_repository)]):    
    try:
      await session_repository.delete_all_sessions(username=user_principal_name)   
    except Exception as err:
      logger.error(err)
      raise HTTPException(status_code=500, detail='Internal Server Error')    