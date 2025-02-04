from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Database settings
    DB_HOST: str = "localhost"
    DB_PORT: int = 3302
    DB_USER: str = "root"
    DB_PASSWORD: str
    DB_NAME: str = "editor_voz_db"
    
    # JWT settings
    JWT_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI settings
    OPENAI_API_KEY: str
    
    # Voice settings
    VOICE_SAMPLES_DIR: str = "voice_samples"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()