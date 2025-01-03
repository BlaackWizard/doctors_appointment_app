import asyncio

import pytz
from fastapi_mail import FastMail, MessageSchema

from src.utils.config_email import conf

from .celery import celery_app

tz = pytz.timezone("Asia/Tashkent")


@celery_app.task
def send_confirmation_email(patient_email, message):
    asyncio.run(_send_confirmation_email(patient_email, message))
    return f"Письмо подтверждения отправлено на {patient_email}"


async def _send_confirmation_email(patient_email, message):
    message = MessageSchema(
        subject="Подтверждение записи",
        recipients=[patient_email],
        body=message,
        subtype="plain",
    )
    fm = FastMail(conf)
    await fm.send_message(message)


@celery_app.task
def send_reminder_email(patient_email, appointment_date, time_remaining):
    asyncio.run(_send_reminder_email(patient_email, appointment_date, time_remaining))
    return f"Напоминание отправлено на {patient_email}"


async def _send_reminder_email(patient_email, appointment_date, time_remaining):
    appointment_date_tz = appointment_date.astimezone(tz)
    message = MessageSchema(
        subject="Напоминание о записи",
        recipients=[patient_email],
        body=f"Напоминаем, что ваша запись состоится {appointment_date_tz}. Осталось {time_remaining}.",
        subtype="plain",
    )
    fm = FastMail(conf)
    await fm.send_message(message)
