from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_user: str = "admin"
    db_password: str = "12345"
    db_name: str = "avito"
    secret_key: str = "very-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env.example"

settings = Settings()