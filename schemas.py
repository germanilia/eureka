from enum import StrEnum
import json
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


class MessageSpeaker(StrEnum):
    ai = "ai"
    user = "user"


class MessageObject(BaseModel):
    speaker: MessageSpeaker = Field(
        ..., description="The name or identifier of the speaker"
    )
    timestamp: datetime = Field(..., description="The time when the message was sent")
    content: str = Field(..., description="The content of the message")

    @staticmethod
    def from_json_list(conversation_history: str) -> List["MessageObject"]:
        # Parse the JSON string into a list of dictionaries
        messages = json.loads(conversation_history)

        # Convert each message to the format expected by the LLM
        formatted_messages: List[MessageObject] = []
        for message in messages:
            formatted_messages.append(MessageObject(**message))

        return formatted_messages

    @staticmethod
    def to_json_list(messages: List["MessageObject"]) -> str:
        def serialize_datetime(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError("Type not serializable")

        return json.dumps([msg.dict() for msg in messages], default=serialize_datetime)


class UserBase(BaseModel):
    first_name: Optional[str] = Field(None, description="The user's first name")
    last_name: Optional[str] = Field(None, description="The user's last name")
    age: Optional[int] = Field(None, description="The user's age")
    email: Optional[EmailStr] = Field(None, description="The user's email address")


class UserCreate(UserBase):
    # For creating a user, we don't need any additional fields
    pass


class UserUpdate(UserBase):
    # For updating a user, all fields are optional
    pass


class User(UserBase):
    id: int = Field(..., description="The unique identifier for the user")
    last_active: datetime = Field(..., description="The last time the user was active")

    class Config:
        orm_mode = True


class ConversationBase(BaseModel):
    messages: List[MessageObject] = Field(
        ..., description="List of messages in the conversation"
    )


class ConversationCreate(ConversationBase):
    user_id: int = Field(
        ..., description="The ID of the user who started the conversation"
    )


class Conversation(ConversationBase):
    id: int = Field(..., description="The unique identifier for the conversation")
    user_id: int = Field(
        ..., description="The ID of the user associated with this conversation"
    )

    class Config:
        orm_mode = True
        from_attributes = True


class MessageInput(BaseModel):
    user_id: int = Field(..., description="The ID of the user sending the message")
    content: str = Field(..., description="The content of the message")
