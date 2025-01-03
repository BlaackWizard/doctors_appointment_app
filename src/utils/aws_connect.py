import boto3

from src.utils.config_aws import settings

session = boto3.session.Session()
s3 = session.client(
    service_name=settings.SERVICE_NAME,
    endpoint_url=settings.ENDPOINT_URL,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)
