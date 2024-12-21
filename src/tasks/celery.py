from celery import Celery

celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    include=['src.tasks.send_email'],
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
)
