# repository/session_repository.py
import os
import threading
from azure.cosmos.aio import ContainerProxy
from typing import List, Optional
from models import Session, Message
import logging

logging.basicConfig(level=logging.INFO)

class SessionRepository:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls,*args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SessionRepository, cls).__new__(cls)             
        return cls._instance

    def __init__(self, container: ContainerProxy):
        self.container = container
                                                  
    async def create_new_session(self, session: Session) -> Session:                
        await self.container.create_item(session.model_dump(by_alias=True))
        return session

    async def get_all_sessions(self, user_name: str) -> List[Session]:
        sessions = []
        query = "SELECT DISTINCT * FROM c where c.type = 'Session' and c.username = @username"
        async for item in self.container.query_items(query=query,
                                                     parameters=[{"name": "@username", "value": str(user_name)}]):
            session = Session.model_validate(item)
            sessions.append(session)
        return sessions     

    async def get_session(self, session_id: str, username: str) -> Optional[Session]:
        logging.info(f"Session ID: {session_id}")
        query = "SELECT * FROM c WHERE c.id = @id AND c.type = 'Session' and c.username = @username"
        async for item in self.container.query_items(query=query, 
                                                     parameters=[{"name": "@id", "value": session_id},
                                                                 {"name": "@username", "value": username}]):
            logging.info(f"Item: {item}")
            session = Session.model_validate(item)
            return session
        return None

    async def update_session(self, session: Session) -> Session:
        await self.container.upsert_item(session.model_dump(by_alias=True))
        return session

    async def get_session_messages(self, session_id: str, username: str) -> List[Message]:
        messages = []
        query = "SELECT * from c WHERE c.sessionId = @sessionId and c.type = 'Message' and c.username = @username"
        async for item in self.container.query_items(query=query, 
                                                     parameters=[{"name": "@sessionId", "value": session_id},
                                                                 {"name": "@username", "value": username}]):  
            message = Message.model_validate(item)
            messages.append(message)
        return messages
                    
    async def delete_session(self, session_id: str, username: str) -> None:
        operations = []
        query = "SELECT c.id FROM c WHERE c.sessionId = @sessionId and c.username = @username"
        async for item in self.container.query_items(query,
                                                     parameters=[{"name": "@sessionId", "value": session_id},
                                                                 {"name": "@username", "value": username}]):
            delete_operation = ("delete", (str(item['id']),))
            operations.append(delete_operation)
        
        if operations:
            partition_key = [username, session_id]
            await self.container.execute_item_batch(batch_operations=operations, partition_key=partition_key)       

    async def delete_all_sessions(self, username: str) -> None:
        operations = []
        query = "SELECT c.id FROM c WHERE c.username = @username AND c.type = 'Session'"
        async for item in self.container.query_items(query,
                                                     parameters=[{"name": "@username", "value": username}]):
            query_session = "SELECT c.id FROM c WHERE c.sessionId = @sessionId"
            async for sessions in self.container.query_items(query_session,
                                                             parameters=[{"name": "@sessionId", "value": item['id']}]):   
                delete_operation = ("delete", (str(sessions['id']),))
                operations.append(delete_operation)
            if operations:
                partition_key = [username, item['id']]
                await self.container.execute_item_batch(batch_operations=operations, partition_key=partition_key)
                operations.clear() 

    async def insert_message_session(self, message: Message) -> Message:          
        await self.container.create_item(message.model_dump(by_alias=True))
        return message
