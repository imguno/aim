import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # 설정에 맞게 수정

app = Celery('aim')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()