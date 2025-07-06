import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoinvoice_generator.settings')

app = Celery('autoinvoice_generator')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
