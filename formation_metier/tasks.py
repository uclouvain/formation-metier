from celery import shared_task
from django.conf import settings
import requests
import logging
from pprint import pprint

from typing import List, Dict

from django.contrib.auth.models import User
from django.db.models import QuerySet

from formation_metier import celery_app

from formation_metier.exemple_data_from_api import data_person
from formation_metier.models.employe_uclouvain import EmployeUCLouvain, RoleFormationFareEnum

logger = logging.getLogger(settings.DEFAULT_LOGGER)


# Commande pour lancer Celery avec exécution du beat :  celery -A formation_metier worker -B -l INFO


@celery_app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@celery_app.task
def get_person_from_osis() -> List[Dict]:
    # En attendant de faire les vrai appel API
    create_person_object_from_api_response(data_person)
    url = settings.API_PERSON_URL + "employeucl/"
    try:
        persons = requests.get(
            url,
            timeout=20
        )
        for item in persons.json():
            print(item)
        # a décommenter lorsque il y aura la vrai API
        # create_person_object_from_api_response(persons.json())
        return persons.json()
    except Exception:
        logger.info("[Synchronize person] An error occurred during fetching person from OSIS")
        raise ValueError


@celery_app.task()
def get_specific_person_from_osis(person_id: str) -> List[Dict]:
    url = settings.API_PERSON_URL + "employeucl/" + str(person_id)
    try:
        person = requests.get(
            url,
            timeout=20  # settings.REQUESTS_TIMEOUT or 20
        )
        return person.json()
    except Exception:
        logger.info("[Synchronize person] An error occurred during fetching person from OSIS")
        raise ValueError


def create_person_object_from_api_response(person_list_json: list):
    print("passé dans creation de person")
    if not person_list_json:
        raise AssertionError
    if type(person_list_json) != list:
        raise TypeError
    else:
        for person in person_list_json:

            name = str(person["firstname"]) + " " + str(person["lastname"])
            numbers_fgs = person["matric_fgs"]
            user_object = User.objects.filter(username=name)
            print(name)
            print(user_object)
            if not user_object:
                user_object = User.objects.create_user(username=name, password="osis")
            if type(user_object) is QuerySet:
                print(type(user_object[0]))
                print(user_object[0])
                person_object = EmployeUCLouvain(name=name,
                                                 numberFGS=numbers_fgs,
                                                 role_formation_metier=RoleFormationFareEnum.PARTICIPANT,
                                                 user=user_object[0]
                                                 )
            else:
                print(type(user_object))
                print(user_object)
                person_object = EmployeUCLouvain(name=name,
                                                 numberFGS=numbers_fgs,
                                                 role_formation_metier=RoleFormationFareEnum.PARTICIPANT,
                                                 user=user_object
                                                 )
            if not EmployeUCLouvain.objects.filter(numberFGS=person_object.numberFGS):
                person_object.save()
