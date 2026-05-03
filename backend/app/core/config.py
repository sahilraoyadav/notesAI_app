from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "NotesAI"
    database_url: str = "sqlite+aiosqlite:///./notesai.db"
    storage_path: str = "backend/storage"
    openai_api_key: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
