import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/codeward"
    JWT_SECRET_KEY: str = "Y0u.Ar3)Cr@zy^1f/Tr1£H4ck¢Th1s}"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

settings = Settings()
