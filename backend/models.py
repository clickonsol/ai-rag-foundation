from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    user_id: Optional[str] = None
    message: str
    timestamp: Optional[datetime] = None

class ChatThread(BaseModel):
    id: str
    thread_name: str
    last_active: datetime

class UserProfile(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    address: str

class Document(BaseModel):
    id: str
    name: str
    download_link: str
