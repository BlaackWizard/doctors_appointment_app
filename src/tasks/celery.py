from celery import Celery

from src.config import settings

celery_app = Celery(
    'tasks',
    broker=settings.BROKER,
    include=['src.tasks.send_email'],
)


celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
)
