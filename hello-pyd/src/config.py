from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    agent_name: str = "hello-agent"
    model_name: str = "gpt-4"
    model_provider: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
