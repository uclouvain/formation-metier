import uuid
from django.conf import settings
import requests
import logging

from typing import List, Dict

from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from rest_framework.exceptions import APIException

from formation_metier import celery_app

from formation_metier.exemple_data_from_api import data_employe_ucl
from formation_metier.models.employe_uclouvain import EmployeUCLouvain, RoleFormationFareEnum

logger = logging.getLogger(settings.DEFAULT_LOGGER)


# Commande pour lancer Celery avec exécution du beat :  celery -A formation_metier worker -B -l INFO

class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'


@celery_app.task
def get_employes_uclouvain_from_osis() -> List[Dict]:
    # En attendant de faire les vrai appel API
    # create_employe_ucl_object_from_api_response(data_employe_ucl)
    # url = settings.API_GET_EMPLOYE_UCL_URL + "employes_ucl/"

    if not all([settings.API_OSIS_URL, settings.OSIS_EMPLOYER_ENDPOINT]):
        raise ImproperlyConfigured('ESB_API_URL / ESB_ENTITIES_HISTORY_ENDPOINT must be set in configuration')

    endpoint = settings.OSIS_EMPLOYER_ENDPOINT
    url = "{esb_api}/{endpoint}".format(esb_api=settings.API_OSIS_URL, endpoint=endpoint)
    employes_ucl = []
    compteur_page = 1
    print(url)
    try:
        api_response_data = requests.get(
            url,
            headers={"Authorization: settings.OSIS_AUTHORIZATION"},
            timeout=20,
            data={'page': compteur_page,
                  'pageSize': 50},
        )
        employes_ucl += api_response_data.json()
        compteur_page += 1
    except Exception:
        logger.info("[Synchronize employe_ucl] An error occurred during fetching employe_ucl from OSIS")
        raise ServiceUnavailable
    while compteur_page < 4:
        try:
            api_response_data = requests.get(
                url,
                headers={"Authorization: settings.OSIS_AUTHORIZATION"},
                timeout=20,
                data={'page': compteur_page,
                      'pageSize': 50},
            )
            employes_ucl += api_response_data['persons']["person"].json()
            compteur_page += 1
            print(len(employes_ucl))

        except Exception:
            logger.info("[Synchronize employe_ucl] An error occurred during fetching employe_ucl from OSIS")
            raise ServiceUnavailable
    print(employes_ucl)
    # return create_employe_ucl_object_from_api_response(employes_ucl)


@celery_app.task()
def get_specific_employe_uclouvain_from_osis(enploye_ucl_id: uuid.UUID) -> List[Dict]:
    url = settings.API_GET_EMPLOYE_UCL_URL + "employe_ucl/" + str(enploye_ucl_id)
    try:
        employe_ucl = requests.get(
            url,
            timeout=20
        )
        return employe_ucl.json()
    except Exception:
        logger.info("[Synchronize employe_ucl] An error occurred during fetching employe_ucl from OSIS")
        raise ServiceUnavailable


def create_employe_ucl_object_from_api_response(employe_ucl_list_json: list):
    if not employe_ucl_list_json:
        raise AssertionError('Auncune données reçue')
    if type(employe_ucl_list_json) != list:
        raise TypeError('Mauvais type de données reçu, les données doivent être de type list')
    else:
        for employe_ucl in employe_ucl_list_json:
            name = str(employe_ucl["firstname"]) + " " + str(employe_ucl["lastname"])
            numbers_fgs = employe_ucl["matric_fgs"]
            user_object = User.objects.filter(username=name)
            if not user_object:
                user_object = User.objects.create_user(username=name, password="osis")
            if type(user_object) is QuerySet:
                employe_ucl_object = EmployeUCLouvain(name=name,
                                                      number_fgs=numbers_fgs,
                                                      role_formation_metier=RoleFormationFareEnum.PARTICIPANT,
                                                      user=user_object[0]
                                                      )
            else:
                employe_ucl_object = EmployeUCLouvain(name=name,
                                                      number_fgs=numbers_fgs,
                                                      role_formation_metier=RoleFormationFareEnum.PARTICIPANT,
                                                      user=user_object
                                                      )
            if not EmployeUCLouvain.objects.filter(number_fgs=employe_ucl_object.number_fgs):
                employe_ucl_object.save()
