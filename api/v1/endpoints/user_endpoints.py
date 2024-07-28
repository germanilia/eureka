from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import UserCreate, UserUpdate, User
from dao.user_dao import UserDAO

router = APIRouter()

@router.post("/users/", response_model=User)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)) -> User:
    user_dao = UserDAO(db)
    return await user_dao.create(user_data)

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> User:
    user_dao = UserDAO(db)
    user = await user_dao.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)) -> User:
    user_dao = UserDAO(db)
    user = await user_dao.update(user_id, user_data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)) -> None:
    user_dao = UserDAO(db)
    user = await user_dao.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await user_dao.delete(user_id)