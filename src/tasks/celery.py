from celery import Celery

from src.config import settings

celery_app = Celery(
    'tasks',
    broker=settings.CELERY_BROKER,
    include=['src.tasks.send_email'],
)


celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    enable_utc=True,
    timezone='Asia/Tashkent',
    broker_connection_retry_on_startup=True,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)
