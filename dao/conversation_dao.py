from sqlalchemy.orm import Session
from sqlalchemy import func
import models
import schemas
from datetime import datetime, timedelta

class ConversationDAO:
    @staticmethod
    def get_or_create(db: Session, user_id: int):
        one_day_ago = datetime.utcnow() - timedelta(days=1)
        conversation = db.query(models.Conversation).filter(
            models.Conversation.user_id == user_id,
            func.json_extract(models.Conversation.messages, '$[0].timestamp') > one_day_ago
        ).order_by(models.Conversation.id.desc()).first()

        if not conversation:
            conversation = models.Conversation(user_id=user_id, messages=[])
            db.add(conversation)
            db.commit()
            db.refresh(conversation)

        return conversation

    @staticmethod
    def add_message(db: Session, conversation: models.Conversation, message: schemas.MessageObject):
        conversation.messages = conversation.messages + [message.dict()]
        db.commit()
        db.refresh(conversation)
        return conversation