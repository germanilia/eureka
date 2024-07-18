from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class MessageObject(BaseModel):
    speaker: str
    timestamp: datetime
    content: str

class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    last_active: datetime

    class Config:
        orm_mode = True

class ConversationBase(BaseModel):
    messages: List[MessageObject]

class ConversationCreate(ConversationBase):
    user_id: int

class Conversation(ConversationBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class MessageInput(BaseModel):
    user_id: int
    content: str