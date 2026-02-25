from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "HBF MLOps API"
    ENVIRONMENT: str = "local"

    KEY_VAULT_NAME: str | None = None
    STORAGE_ACCOUNT_NAME: str | None = None   # 👈 ADD THIS

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()