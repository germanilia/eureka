from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

import models
from schemas import Conversation, MessageObject
from datetime import datetime


class ConversationDAO:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_or_create(self, user_id: int) -> models.Conversation:
        # Get the start of the current day in UTC
        today_start = datetime.utcnow().replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        # Construct the query
        query = (
            select(models.Conversation)
            .where(
                models.Conversation.user_id == user_id,
                models.Conversation.last_updated >= today_start,
            )
            .order_by(models.Conversation.last_updated.desc())
            .limit(1)
        )

        # Execute the query
        result = await self.db.execute(query)
        conversation = result.scalar_one_or_none()

        if not conversation:
            # If no conversation found today, create a new one
            conversation = models.Conversation(user_id=user_id, messages=[])
            self.db.add(conversation)
            await self.db.commit()
            await self.db.refresh(conversation)
        return conversation

    async def add_messages(
        self, conversation_id: int, messages: List[MessageObject]
    ) -> Conversation:
        # First, fetch the existing conversation
        stmt = select(models.Conversation).where(
            models.Conversation.id == conversation_id
        )
        result = await self.db.execute(stmt)
        conversation = result.scalar_one()
        existing_messages: List[MessageObject] = MessageObject.from_json_list(
            str(conversation.messages)
        )

        updated_messages = existing_messages + messages

        # Convert all messages back to JSON
        updated_messages_json = MessageObject.to_json_list(updated_messages)

        # Update the conversation without RETURNING clause
        update_stmt = (
            update(models.Conversation)
            .where(models.Conversation.id == conversation_id)
            .values(messages=updated_messages_json)
        )
        await self.db.execute(update_stmt)
        await self.db.commit()

        # Fetch the updated conversation
        fetch_stmt = select(models.Conversation).where(
            models.Conversation.id == conversation_id
        )
        result = await self.db.execute(fetch_stmt)
        updated_conversation = result.scalar_one()
        return Conversation(
            messages=MessageObject.from_json_list(updated_conversation.messages), # type: ignore
            id=updated_conversation.id, # type: ignore
            user_id=updated_conversation.user_id, # type: ignore
        )
        # updated_conversation = Conversation.from_orm(updated_conversation)
        # # updated_conversation.messages = MessageObject.from_json_list(updated_conversation.messages)
        # return updated_conversation
