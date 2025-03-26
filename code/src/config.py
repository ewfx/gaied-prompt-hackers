from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Email Classification System"
    DEBUG: bool = True
    LLM_API_KEY: str = ""
    TEMP_STORAGE_PATH: str = "temp_storage"

settings = Settings()
