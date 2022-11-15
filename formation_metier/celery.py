import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'module_formation.settings')

app = Celery('formation_metier')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'
app.conf.timezone = 'Europe/Belgium'

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'get_person_every_day': {
        'task': 'tasks.get_person_from_osis',
        'schedule': crontab(minute="*/30"),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
