from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models

class UserDAO:
    @staticmethod
    async def get_or_create(db: AsyncSession, user_id: int):
        result = await db.execute(select(models.User).filter(models.User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            user = models.User(id=user_id)
            db.add(user)
            await db.commit()
            await db.refresh(user)
        return user

    @staticmethod
    async def get_conversations(db: AsyncSession, user_id: int):
        user = await UserDAO.get_or_create(db, user_id)
        return user.conversations