from celery import shared_task
from django.conf import settings
import requests
import logging
from formation_metier.models.person import create_person_object_from_api_response

logger = logging.getLogger(settings.DEFAULT_LOGGER)


@shared_task
def get_person_from_osis():
    url = settings.API_PERSON_URL + "person/"
    print(url)
    try:
        persons = requests.get(
            url,
            timeout=20  # settings.REQUESTS_TIMEOUT or 20
        )
        for item in persons:
            print(item)
        create_person_object_from_api_response(persons.json())
        return persons.json()
    except Exception:
        logger.info("[Synchronize person] An error occurred during fetching person from OSIS")
        raise ValueError


@shared_task
def get_specific_person_from_osis(person_id):
    url = settings.API_PERSON_URL + "person/" + str(person_id)
    print(url)
    try:
        person = requests.get(
            url,
            timeout=20  # settings.REQUESTS_TIMEOUT or 20
        )
        print(person)
        print(person.json())
        # create_person_object_from_api_response(person.json())
        return person.json()
    except Exception:
        logger.info("[Synchronize person] An error occurred during fetching person from OSIS")
        raise ValueError
