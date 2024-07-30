from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    token: str
    admin: str
    redis: str

    class Config:
        env_file = ".env"


settings = Settings()
