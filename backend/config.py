from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AES_ENCRYPTION_KEY: str
    DATABASE_URL: str = "postgresql://postgres:321@localhost:5432/mydatabase" 

    class Config:
        env_file = ".env"

settings = Settings()