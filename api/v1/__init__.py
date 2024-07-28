from fastapi import APIRouter
from .endpoints.conversation_endpoints import router as conversation
from .endpoints.user_endpoints import router as user


api_router = APIRouter()
api_router.include_router(conversation, prefix="/conversation")
api_router.include_router(user, prefix="/users")
