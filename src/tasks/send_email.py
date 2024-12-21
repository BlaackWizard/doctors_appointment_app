import asyncio
from datetime import timedelta

from fastapi_mail import FastMail, MessageSchema

from src.utils.config_email import conf

from .celery import celery_app


@celery_app.task
def send_confirmation_email(patient_email, html_message):
    asyncio.run(_send_confirmation_email(patient_email, html_message))
    return f"Письмо подтверждения отправлено на {patient_email}"


async def _send_confirmation_email(patient_email, html_message):
    message = MessageSchema(
        subject="Подтверждение записи",
        recipients=[patient_email],
        body=html_message,
    )
    fm = FastMail(conf)
    await fm.send_message(message)


@celery_app.task
def send_reminder_email(patient_email, appointment_date, reminder_time):
    asyncio.run(_send_reminder_email(patient_email, appointment_date, reminder_time))
    return f"Напоминание отправлено на {patient_email}"


async def _send_reminder_email(patient_email, appointment_date, reminder_time):
    message = MessageSchema(
        subject="Напоминание о записи",
        recipients=[patient_email],
        body=f"Напоминаем, что ваша запись состоится {appointment_date}. Осталось {reminder_time}.",
        subtype="plain",
    )
    fm = FastMail(conf)
    await fm.send_message(message)


def schedule_appointment_notifications(appointment, patient_email):
    send_confirmation_email.delay(patient_email, appointment.date)

    reminder_24h_time = appointment.date - timedelta(hours=24)
    send_reminder_email.apply_async(
        (appointment.patient_email, appointment.date, "24 часа"),
        eta=reminder_24h_time,
    )

    reminder_1h_time = appointment.date - timedelta(hours=1)
    send_reminder_email.apply_async(
        (appointment.patient_email, appointment.date, "1 час"),
        eta=reminder_1h_time,
    )
