from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from llm.llm_manager import LLMManager, LLMModels
# from models import Conversation
from schemas import Conversation as ConversationSchema, MessageInput
from database import get_db
from typing import List
from services import ConversationManager

router = APIRouter()


@router.post("/conversations/", response_model=ConversationSchema)
async def send_message(
    message_input: MessageInput, db: AsyncSession = Depends(get_db)
) -> ConversationSchema:
    """
    Send a message and get a response from the AI.

    - **user_id**: ID of the user sending the message
    - **content**: Content of the message
    """
    conversation_manager = ConversationManager(db)
    llm = LLMManager.get_llm(LLMModels.claude_haiku)
    response = await conversation_manager.process_user_message(
        message_input=message_input, llm=llm
    )
    
    return response


@router.get("/conversations/{user_id}", response_model=List[ConversationSchema])
async def get_user_conversations(user_id: int, db: AsyncSession = Depends(get_db)) -> List[ConversationSchema]:
    """
    Retrieve all conversations for a specific user.

    - **user_id**: ID of the user whose conversations to retrieve
    """
    conversation_manager = ConversationManager(db)
    conversations = await conversation_manager.get_user_conversations(user_id)
    return [ConversationSchema.model_validate(conv) for conv in conversations]
