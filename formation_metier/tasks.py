from celery import shared_task
from django.conf import settings
import requests
import logging

logger = logging.getLogger(settings.DEFAULT_LOGGER)


@shared_task
def get_person_from_osis():
    url = settings.API_PERSON_URL
    try:
        persons = requests.get(
            url,
            timeout=20  # settings.REQUESTS_TIMEOUT or 20
        )
        return persons.json()
    except Exception:
        logger.info("[Synchronize entities] An error occurred during fetching person from OSIS")
        raise ValueError
