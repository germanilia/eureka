import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Determine the environment
ENV = os.getenv("ENV", "dev")

# Load the appropriate .env file
load_dotenv(f".env.{ENV.lower()}")

class Settings(BaseSettings):
    ENV: str = ENV
    DEBUG: bool = False
    APP_NAME: str = "Eureka - Conversation Agent"
    APP_VERSION: str = "0.1.0"
    MODEL_NAME: str = os.getenv("MODEL_NAME", "anthropic.claude-3-5-sonnet-20241022-v2:0")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 3306))
    DB_USER: str = os.getenv("DB_USER", "")
    DB_PASS: str = os.getenv("DB_PASS", "")
    DB_NAME: str = os.getenv("DB_NAME", "")
    SUPERSECRETKEY: str = os.getenv("SUPERSECRETKEY", "Cowabunga")

    class Config:
        env_file = f"config/.env.{ENV.lower()}"
        env_file_encoding = 'utf-8'
        load_dotenv(env_file)
    
    @property
    def DATABASE_URL(self):
        connection_string = f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        print(f"connectoin string: {connection_string}")
        return connection_string


# Instantiate the Settings class
settings = Settings()