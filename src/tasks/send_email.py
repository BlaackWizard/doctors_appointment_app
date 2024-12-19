import logging
import smtplib
from email.message import EmailMessage

from celery import shared_task

from src.utils.config_email import email_settings

logger = logging.getLogger(__name__)


@shared_task
def send_email(to_email: str, subject: str, body: str):
    try:
        logger.info(f"Отправка письма на {to_email} с темой: {subject}")
        smtp_server = email_settings.SMTP_SERVER
        smtp_port = email_settings.SMTP_PORT
        smtp_user = email_settings.SMTP_USER
        smtp_password = email_settings.SMTP_PASS

        msg = EmailMessage()
        msg["From"] = smtp_user
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        logger.info(f"Письмо успешно отправлено на {to_email}")
        return f"Письмо отправлено на {to_email}"
    except Exception as e:
        logger.error(f"Ошибка при отправке письма: {e}")
        return f"Не удалось отправить письмо: {e}"
