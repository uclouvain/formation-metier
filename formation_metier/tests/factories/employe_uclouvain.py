import random
import string

import factory
import factory.fuzzy
from django.contrib.auth.models import Group, Permission

from formation_metier.models.employe_uclouvain import RoleFormationFareEnum
from formation_metier.tests.factories.user import UserFactory


def add_employe_uclouvain_to_groups(employe_uclouvain, groups):
    if type(groups) == str:
        employe_uclouvain.user.groups.add(Group.objects.get_or_create(name=groups)[0])
    else:
        groups_obj = [Group.objects.get_or_create(name=name)[0] for name in groups]
        employe_uclouvain.user.groups.add(*groups_obj)


def generate_matricule_fgs() -> str:
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
    matricule_fgs = factory.LazyFunction(generate_matricule_fgs)


class EmployeUCLouvainFormateurFactory(EmployeUCLouvainFactory):
    role_formation_metier = RoleFormationFareEnum.FORMATEUR


class EmployeUCLouvainParticipantFactory(EmployeUCLouvainFactory):
    role_formation_metier = RoleFormationFareEnum.PARTICIPANT


class EmployeUCLouvainWithPermissionsFactory:
    def __init__(self, *permissions, groups=None, role=None, **kwargs):
        perms_obj = [Permission.objects.get_or_create(defaults={"name": p}, codename=p)[0] for p in permissions]

        if role:
            if role == RoleFormationFareEnum.PARTICIPANT:
                self.employe_uclouvain = EmployeUCLouvainParticipantFactory(**kwargs)
            if role == RoleFormationFareEnum.FORMATEUR:
                self.employe_uclouvain = EmployeUCLouvainFormateurFactory(**kwargs)
        else:
            self.employe_uclouvain = EmployeUCLouvainFactory(**kwargs)
        if groups:
            add_employe_uclouvain_to_groups(self.employe_uclouvain, groups)
        self.employe_uclouvain.user.user_permissions.add(*perms_obj)

    def __new__(cls, *permissions, **kwargs):
        obj = super().__new__(cls)
        obj.__init__(*permissions, **kwargs)
        return obj.employe_uclouvain
