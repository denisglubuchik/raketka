import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    token: str = os.getenv("token")
    admin: str = os.getenv("admin")
    ref: str = os.getenv("ref")
    db: int = os.getenv("db")


settings = Settings()
