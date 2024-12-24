from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    CELERY_BROKER: str
    API_PORT: int
    DOMAIN: str

    class Config:
        env_file = ".env"

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
