from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "mysql+aiomysql://editor_user:editor_password@db:3306/editor_voz_db"
    DB_HOST: str = "db"
    DB_PORT: int = 3306
    DB_USER: str = "editor_user"
    DB_PASSWORD: str = "editor_password"
    DB_NAME: str = "editor_voz_db"
    MYSQL_ROOT_PASSWORD: str = "root_password"
    
    # JWT settings
    JWT_SECRET: str = "your_super_secret_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI settings
    OPENAI_API_KEY: str = "your_openai_key"
    
    # Voice settings
    VOICE_SAMPLES_DIR: str = "voice_samples"
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

@lru_cache()
def get_settings() -> Settings:
    return Settings()