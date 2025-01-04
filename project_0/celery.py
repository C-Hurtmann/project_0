import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_0.settings')

app = Celery('project_0', broker_connection_retry_on_startup=True)
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(related_name='tasks')
app.autodiscover_tasks(related_name='signals')
