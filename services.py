from sqlalchemy.ext.asyncio import AsyncSession
from schemas import MessageInput, MessageObject
from dao.user_dao import UserDAO
from dao.conversation_dao import ConversationDAO
from llm.conversation import LLMConversation
from datetime import datetime

llm_conversation = LLMConversation()

async def process_user_message(db: AsyncSession, message_input: MessageInput):
    user = await UserDAO.get_or_create(db, message_input.user_id)
    conversation = await ConversationDAO.get_or_create(db, user.id)

    user_message = MessageObject(
        speaker="user",
        timestamp=datetime.utcnow(),
        content=message_input.content
    )
    conversation = await ConversationDAO.add_message(db, conversation, user_message)

    llm_response = await llm_conversation.generate_response(message_input.content)
    llm_message = MessageObject(
        speaker="ai",
        timestamp=datetime.utcnow(),
        content=llm_response
    )
    conversation = await ConversationDAO.add_message(db, conversation, llm_message)

    return conversation

async def get_user_conversations(db: AsyncSession, user_id: int):
    return await UserDAO.get_conversations(db, user_id)