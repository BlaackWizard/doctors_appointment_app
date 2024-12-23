from pydantic_settings import BaseSettings


class AWSSettings(BaseSettings):
    SERVICE_NAME: str
    ENDPOINT_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    BUCKET_NAME: str

    class Config:
        env_file = ".env_aws"


settings = AWSSettings()
