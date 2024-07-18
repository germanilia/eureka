from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import schemas
import services
from database import get_db
from config.config import settings
from typing import List

app = FastAPI(
    title=settings.APP_NAME,
    description="A FastAPI project with SQLAlchemy, MySQL, and Swagger UI",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

@app.post("/send_message/", response_model=schemas.Conversation)
async def send_message(message_input: schemas.MessageInput, db: AsyncSession = Depends(get_db)):
    """
    Send a message and get a response from the AI.

    - **user_id**: ID of the user sending the message
    - **content**: Content of the message
    """
    return await services.process_user_message(db, message_input)

@app.get("/conversations/{user_id}", response_model=List[schemas.Conversation])
async def get_user_conversations(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve all conversations for a specific user.

    - **user_id**: ID of the user whose conversations to retrieve
    """
    return await services.get_user_conversations(db, user_id)