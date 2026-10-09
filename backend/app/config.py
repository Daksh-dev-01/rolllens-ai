from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    app_name: str = "RollLens AI API"
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./rolllens_demo.db"
    storage_dir: Path = Path("./private_uploads")
    max_upload_mb: int = 25
    demo_mode: bool = True
    model_config = SettingsConfigDict(env_file=".env", env_prefix="ROLLLENS_", extra="ignore")

settings = Settings()
