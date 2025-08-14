import os

class Settings:
    DB_PATH: str = os.getenv("DB_PATH", "app/data/lab.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "insecure-dev-secret")  # intencionalmente débil
    CHAOS_RATE: float = float(os.getenv("CHAOS_RATE", "0.0"))  # 0.0 a 1.0

settings = Settings()
