from django.db import models
from formation_metier.enums.roles_osis_enum import ROLES_OSIS_CHOICES


class Person(models.Model):
    name = models.CharField(max_length=50, blank=False)
    numberFGS = models.CharField(max_length=8, blank=False)
    role_formation_metier = models.CharField(choices=ROLES_OSIS_CHOICES, max_length=50, default=None, blank=True)

    def __str__(self):
        return f"{self.name}"


def create_person_object_from_api_response(person_list_json: list):
    if not person_list_json:
        raise AssertionError
    if type(person_list_json) != list:
        raise TypeError
    else:
        for person in person_list_json:
            print(person)
