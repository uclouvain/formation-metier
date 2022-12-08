import uuid
from django.conf import settings
import requests
import logging

from typing import List, Dict

from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from rest_framework.exceptions import APIException

from formation_metier import celery_app
from formation_metier.models.employe_uclouvain import EmployeUCLouvain, RoleFormationFareEnum

logger = logging.getLogger(settings.DEFAULT_LOGGER)


# Commande pour lancer Celery avec exécution du beat :  celery -A formation_metier worker -B -l INFO

class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'


@celery_app.task
def run():
    if not all([settings.API_OSIS_URL, settings.OSIS_EMPLOYER_ENDPOINT]):
        raise ImproperlyConfigured('ESB_API_URL / ESB_ENTITIES_HISTORY_ENDPOINT must be set in configuration')
    employes_ucl = []
    try:
        compteur_page = 1
        page_size = 50
        while compteur_page < 200:
            data_from_api = get_employes_uclouvain_from_osis(compteur_page, page_size)
            compteur_page += 1
            employes_ucl += data_from_api["persons"]["person"]
            if len(data_from_api["persons"]["person"]) < 50:
                break
        create_employe_ucl_object_from_api_response(employes_ucl)
        return {'Employe UCLouvain synchronized': 'OK'}
    except ServiceUnavailable:
        return {'Employe UCLouvain synchronized': 'Unable to fetch data from OSIS'}


def get_employes_uclouvain_from_osis(compteur_page, page_size) -> List[Dict]:
    url = "{osis_api}/{endpoint}".format(osis_api=settings.API_OSIS_URL,
                                         endpoint=settings.OSIS_EMPLOYER_ENDPOINT.format(page=compteur_page,
                                                                                         pageSize=page_size))
    try:
        api_response_data = requests.get(
            url,
            headers={"Authorization": "Bearer " + settings.OSIS_AUTHORIZATION},
            timeout=20,
        )
        return api_response_data.json()
    except Exception:
        logger.info("[Synchronize employe_ucl] An error occurred during fetching employe_ucl from OSIS")
        raise ServiceUnavailable


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
            if str(employe_ucl["lastname"]) == ".":
                name = str(employe_ucl["firstname"])
            elif str(employe_ucl["firstname"]) == ".":
                name = str(employe_ucl["lastname"])
            else:
                name = str(employe_ucl["firstname"]) + " " + str(employe_ucl["lastname"])
            number_fgs = employe_ucl["matric_fgs"]
            if not User.objects.filter(employeuclouvain__number_fgs=number_fgs).exists():
                user_object = User.objects.create_user(username=number_fgs,
                                                       password="password123")
                EmployeUCLouvain.objects.update_or_create(name=name,
                                                          number_fgs=number_fgs,
                                                          role_formation_metier=RoleFormationFareEnum.PARTICIPANT,
                                                          user=user_object
                                                          )
            else:
                user_object = User.objects.get(employeuclouvain__number_fgs=number_fgs)
                EmployeUCLouvain.objects.update_or_create(name=name,
                                                          number_fgs=number_fgs,
                                                          role_formation_metier=RoleFormationFareEnum.PARTICIPANT,
                                                          user=user_object
                                                          )
