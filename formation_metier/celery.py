import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'module_formation.settings')
app = Celery('formation_metier')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'get_employe_ucl_every_day': {
        'task': 'formation_metier.tasks.get_employes_uclouvain_from_osis',
        'schedule': crontab(hour="6"),
    },
    'get_employe_ucl_every_minute': {
        'task': 'formation_metier.tasks.get_employes_uclouvain_from_osis',
        'schedule': crontab(minute="*"),
    },
}
