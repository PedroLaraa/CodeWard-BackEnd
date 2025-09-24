import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://default:zD9lxordAyw0@ep-wild-band-a4snaafu-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require"
    JWT_SECRET_KEY: str = "Y0u.Ar3)Cr@zy^1f/Tr1£H4ck¢Th1s}"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

settings = Settings()
