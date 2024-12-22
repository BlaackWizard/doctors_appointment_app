import logging

from itsdangerous import URLSafeTimedSerializer

from src.utils.config_email import settings

serializer = URLSafeTimedSerializer(
        secret_key=settings.JWT_SECRET_KEY, salt='email-configuration',
)


def create_url_safe_token(data: dict):
    token = serializer.dumps(data)

    return token


def decode_url_safe_token(token: str):
    try:
        token_data = serializer.loads(token)

        return token_data

    except Exception as exc:
        logging.error(str(exc))
