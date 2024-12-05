from langchain_aws import ChatBedrock
from sqlalchemy.ext.asyncio import AsyncSession
from models import Conversation
from schemas import MessageInput, MessageObject, MessageSpeaker
from dao.user_dao import UserDAO
from dao.conversation_dao import ConversationDAO
from llm.conversation import LLMConversation
from datetime import datetime
from typing import List


class ConversationManager:
    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db
        self.user_dao = UserDAO(db)
        self.conversation_dao = ConversationDAO(db)
        self.llm_conversation = LLMConversation()

    async def process_user_message(self, message_input: MessageInput, llm: ChatBedrock) -> Conversation:
        user = await self.user_dao.get_or_create(message_input.user_id)
        conversation = await self.conversation_dao.get_or_create(user.id)  # type: ignore
        conversation_history = conversation.messages

        user_message = MessageObject(
            speaker=MessageSpeaker.user,
            timestamp=datetime.utcnow(),
            content=message_input.content,
        )
        llm_response = await self.llm_conversation.generate_response(
            user_message=user_message,
            llm=llm,
            conversation_history=MessageObject.from_json_list(
                str(conversation_history)
            ),
        )
        conversation = await self.conversation_dao.add_messages(
            conversation_id=conversation.id,  # type: ignore
            messages=[user_message,llm_response]
        )
        return conversation

    async def get_user_conversations(self, user_id: int) -> List[Conversation]:
        return await self.user_dao.get_conversations(user_id)
