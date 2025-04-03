from config import Config
from fastapi import FastAPI
from fastapi import Request, HTTPException
from repository.session_repository import SessionRepository
from services.chat_service import ChatService
from logging import Logger
import logging
import sys

_config = Config()

# This should be set during development mode
# it's easier but you could always inject the
# X-MS-CLIENT-PRINCIPAL-NAME Header
_isDevelopment = _config.is_development()
_user_principal_name = _config.user_principal_name_dev()

# Configure logger
_logger = logging.getLogger('openai_api')

if _config.is_development():
    _logger.setLevel(logging.DEBUG)
else:
    _logger.setLevel(logging.INFO)

# StreamHandler for the console
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
_logger.addHandler(stream_handler)

# ####################################
# Dependency methods using dependency 
# injection in the route
######################################
def get_chat_service(request: Request) -> ChatService:
    return request.app.state.chat_service

def get_session_repository(request: Request) -> SessionRepository:
    return request.app.state.session_repository

def get_easy_auth_token(request: Request)->str:
    if _isDevelopment:
        user_principal_id = _user_principal_name
    else:
        user_principal_id = request.headers.get(key='X-MS-CLIENT-PRINCIPAL-NAME',default=None)
    
    if user_principal_id is None:
        raise HTTPException(401,'No user identity present')
    
    return user_principal_id

def get_logger() -> Logger:
    return _logger