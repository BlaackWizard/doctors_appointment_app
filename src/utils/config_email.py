from pydantic_settings import BaseSettings


class EmailSettings(BaseSettings):
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    class Config:
        env_file = ".env_email"


email_settings = EmailSettings()
