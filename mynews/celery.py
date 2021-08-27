import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mynews.settings")

app = Celery("mynews")

CELERY_TIMEZONE = "Asia/Dhaka"

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

