from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # LiveKit Configuration
    LIVEKIT_API_KEY: str
    LIVEKIT_API_SECRET: str
    LIVEKIT_URL: str = "ws://localhost:7880"
    
    # LLM Configuration
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-pro"
    GEMINI_MAX_TOKENS: int = 2048
    GEMINI_TEMPERATURE: float = 0.7
    
    # CodeVoice TTS Configuration
    CODEVOICE_API_KEY: str
    CODEVOICE_BASE_URL: str = "https://voices.codelessai.in"
    CODEVOICE_VOICE: str = "Ryan"
    CODEVOICE_POLL_INTERVAL: int = 2
    CODEVOICE_MAX_POLLS: int = 60
    
    # Backend Configuration
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"
    
    # Session Configuration
    SESSION_TIMEOUT: int = 1800
    MAX_CONVERSATION_HISTORY: int = 50
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra environment variables


settings = Settings()
