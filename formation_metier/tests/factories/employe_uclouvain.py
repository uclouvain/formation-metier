import random
import string

import factory
import factory.fuzzy
from django.contrib.auth.models import Group, Permission

from formation_metier.models.employe_uclouvain import RoleFormationFareEnum
from formation_metier.tests.factories.user import UserFactory


def add_employe_uclouvain_to_groups(employe_uclouvain, groups):
    groups_obj = [Group.objects.get_or_create(name=name)[0] for name in groups]
    employe_uclouvain.user.groups.add(*groups_obj)


def generate_number_fgs() -> str:
    text_code = [random.choice(string.ascii_uppercase) for _ in range(4)]
    digit_code = [random.choice(string.digits) for _ in range(4)]
    return "".join(text_code + digit_code)


class EmployeUCLouvainFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'formation_metier.EmployeUCLouvain'
        django_get_or_create = ('user',)

    user = factory.SubFactory(UserFactory)
    name = factory.LazyAttribute(lambda employe_uclouvain:
                                 employe_uclouvain.user.username if employe_uclouvain.user else factory.Faker('name'))
    number_fgs = factory.LazyFunction(generate_number_fgs)


class EmployeUCLouvainFormateurFactory(EmployeUCLouvainFactory):
    role_formation_metier = RoleFormationFareEnum.FORMATEUR


class EmployeUCLouvainParticipantFactory(EmployeUCLouvainFactory):
    role_formation_metier = RoleFormationFareEnum.PARTICIPANT


class EmployeUCLouvainWithPermissionsFactory:
    def __init__(self, *permissions, groups=None, **kwargs):
        perms_obj = [Permission.objects.get_or_create(defaults={"name": p}, codename=p)[0] for p in permissions]
        self.employe_uclouvain = EmployeUCLouvainFactory(**kwargs)
        self.employe_uclouvain.user.user_permissions.add(*perms_obj)

        if groups:
            add_employe_uclouvain_to_groups(self.employe_uclouvain, groups)

    def __new__(cls, *permissions, **kwargs):
        obj = super().__new__(cls)
        obj.__init__(*permissions, **kwargs)
        return obj.employe_uclouvain
