import logging

from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from src.config import settings

serializer = URLSafeTimedSerializer(
        secret_key=settings.JWT_SECRET_KEY, salt='email-configuration',
)


def create_url_safe_token(data: dict):
    token = serializer.dumps(data)

    return token


def decode_url_safe_token(token: str, max_age: int = 600):
    try:
        token_data = serializer.loads(token, max_age=max_age)
        return token_data
    except SignatureExpired:
        logging.error("Токен истек")
    except BadSignature:
        logging.error("Неверный токен")
    except Exception as exc:
        logging.error(f"Другая ошибка: {str(exc)}")
    return None
