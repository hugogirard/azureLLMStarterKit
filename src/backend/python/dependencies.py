from config import Config
from fastapi import FastAPI
from fastapi import Request, HTTPException
from repository.session_repository import SessionRepository
from services import ChatService

_config = Config()

# This should be set during development mode
# it's easier but you could always inject the
# X-MS-CLIENT-PRINCIPAL-NAME Header
_isDevelopment = _config.is_development()
_user_principal_name = _config.user_principal_name_dev()


# ####################################
# Dependency methods using dependency 
# injection in the route
######################################
def get_chat_service(app:FastAPI) -> ChatService:
    return app.state.chat_service

def get_session_repository(app:FastAPI) -> SessionRepository:
    return app.state.session_repository

def get_easy_auth_token(request: Request)->str:
    if _isDevelopment:
        user_principal_id = _user_principal_name
    else:
        user_principal_id = request.headers.get(key='X-MS-CLIENT-PRINCIPAL-NAME',default=None)
    
    if user_principal_id is None:
        raise HTTPException(401,'No user identity present')
    
    return user_principal_id