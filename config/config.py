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
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = ""
    DB_PASS: str = ""
    DB_NAME: str = ""

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