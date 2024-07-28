from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from models import User
from schemas import Conversation, UserCreate, UserUpdate, MessageObject
from sqlalchemy.orm import selectinload


class UserDAO:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, user_data: UserCreate) -> User:
        user = User(**user_data.model_dump())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalar_one_or_none()

    async def update(self, user_id: int, user_data: UserUpdate) -> User | None:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(**user_data.model_dump(exclude_unset=True))
        )
        await self.db.execute(stmt)
        await self.db.commit()
        return await self.get(user_id)

    async def delete(self, user_id: int) -> None:
        stmt = delete(User).where(User.id == user_id)
        await self.db.execute(stmt)
        await self.db.commit()

    async def get_or_create(self, user_id: int) -> User:
        try:
            stmt = (
                select(User)
                .options(selectinload(User.conversations))
                .where(User.id == user_id)
            )
            result = await self.db.execute(stmt)
            user = result.scalar_one_or_none()
            if not user:
                user = User(id=user_id)
                self.db.add(user)
                try:
                    await self.db.commit()
                    print(f"User {user_id} committed successfully")
                except Exception as e:
                    print(f"Error during commit: {str(e)}")
                    raise
                try:
                    await self.db.refresh(user)
                    print(f"User {user_id} refreshed successfully")
                except Exception as e:
                    print(f"Error during refresh: {str(e)}")
                    # Instead of raising, let's return the user without refreshing
                    return user
            return user
        except Exception as e:
            print(f"Unexpected error in get_or_create: {str(e)}")
            raise

    async def get_conversations(self, user_id: int) -> List[Conversation]:
        stmt = (
            select(User)
            .options(selectinload(User.conversations))
            .where(User.id == user_id)
        )
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            return []
        conversations: List[Conversation] = []
        for conversation in user.conversations:
            conversations.append(
                Conversation(
                    messages=MessageObject.from_json_list(conversation.messages),  # type: ignore
                    id=conversation.id,  # type: ignore
                    user_id=conversation.user_id,  # type: ignore
                )
            )
        return conversations
