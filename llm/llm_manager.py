from enum import StrEnum
from typing import Optional
import boto3
import logging
from langchain_aws import ChatBedrock
from botocore.config import Config
from config.config import settings

logger = logging.getLogger(__name__)


class LLMModels(StrEnum):
    claude_haiku = "anthropic.claude-3-5-haiku-20241022-v1:0"
    claude_opus = "anthropic.claude-3-opus-20240229-v1:0"
    claude_sonnet = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    claude_sonnet_35 = "anthropic.claude-3-5-sonnet-20241022-v2:0"


class LLMManager:
    @staticmethod
    def get_llm(
        model_name: LLMModels = LLMModels[settings.MODEL_NAME],
        region: str = settings.REGION,
        temperature: float = 0.4,
        credentials_profile: Optional[str] = None,
    ) -> ChatBedrock:
        try:
            client = boto3.client(
                service_name="bedrock-runtime",
                region_name=region,
                config=Config(read_timeout=300),
            )
            if model_name in [LLMModels.claude_opus, LLMModels.claude_sonnet, LLMModels.claude_sonnet_35, LLMModels.claude_haiku]:
                llm = ChatBedrock(
                    client=client,
                    credentials_profile_name=credentials_profile,
                    model=model_name,
                    model_kwargs={
                        "max_tokens": 4096,
                        "stop_sequences": ["\n\nHuman:"],
                        "temperature": temperature,
                        "top_p": 1,
                    },
                )
           
          
            return llm
        except Exception as e:
            logger.error(f"Unable to load model: {e}")
            raise
