import datetime
from typing import List
from langchain_aws import ChatBedrock

from llm.prompts import SYSTEM_MESSAGE_PROMPT
from schemas import MessageObject, MessageSpeaker


class LLMConversation:
    def __init__(self):
        # Initialize any necessary attributes for the LLM conversation
        pass  # Use 'pass' if there's no initialization needed

    async def generate_response(
        self,
        user_message: MessageObject,
        llm: ChatBedrock,
        conversation_history: List[MessageObject],
    ) -> MessageObject:
        messages = (
            [{"role": "system", "content": SYSTEM_MESSAGE_PROMPT}]
            + [
                {
                    "role": MessageSpeaker.user if msg.speaker == MessageSpeaker.user else MessageSpeaker.ai,
                    "content": msg.content,
                }
                for msg in conversation_history
            ]
            + [{"role": MessageSpeaker.user, "content": user_message.content}]
        )

        response = await llm.ainvoke(messages)

        return MessageObject(
            speaker=MessageSpeaker.ai,
            timestamp=datetime.datetime.now(),
            content=str(response.content),
        )
