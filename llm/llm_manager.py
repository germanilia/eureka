from enum import StrEnum
from typing import Optional
import boto3
import logging
from langchain_aws import ChatBedrock
from botocore.config import Config


logger = logging.getLogger(__name__)


class LLMModels(StrEnum):
    claude_haiku = "anthropic.claude-3-haiku-20240307-v1:0"
    claude_opus = "anthropic.claude-3-opus-20240229-v1:0"
    claude_sonnet = "anthropic.claude-3-sonnet-20240229-v1:0"
    claude_sonnet_35 = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    llama3_1_8b_instruct_v1 = "meta.llama3-1-8b-instruct-v1:0"
    llama3_1_70b_instruct_v1  = "meta.llama3-1-70b-instruct-v1:0"
    llama3_1_405b_instruct_v1 = "meta.llama3-1-405b-instruct-v1:0"


class LLMManager:
    @staticmethod
    def get_llm(
        model_name: LLMModels,
        region: str = "us-west-2",
        temperature=0.4,
        credentials_profile: Optional[str] = None,
    ) -> ChatBedrock:
        try:
            client = boto3.client(
                service_name="bedrock-runtime",
                region_name=region,
                config=Config(read_timeout=300),
            )
            if model_name in [LLMModels.llama3_1_405b_instruct_v1, LLMModels.llama3_1_70b_instruct_v1, LLMModels.llama3_1_8b_instruct_v1]:
                llm = ChatBedrock(
                    client=client,
                    credentials_profile_name=credentials_profile,
                    model_id=model_name,
                    model_kwargs={
                        "temperature": temperature,
                        "top_p": 1,
                        "max_gen_len": 4096
                    },
                )
            if model_name in [LLMModels.claude_opus, LLMModels.claude_sonnet, LLMModels.claude_sonnet_35, LLMModels.claude_haiku]:
                llm = ChatBedrock(
                    client=client,
                    credentials_profile_name=credentials_profile,
                    model_id=model_name,
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
