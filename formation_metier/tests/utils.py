from django.contrib.auth.models import User

from formation_metier.models.formation import Formation
from formation_metier.models.seance import Seance
from formation_metier.models.register import Register
from formation_metier.models.employe_uclouvain import EmployeUCLouvain


def create_test_employe_ucl(name, number_fgs, role_formation_metier, user=None):
    return EmployeUCLouvain.objects.create(name=name,
                                           numberFGS=number_fgs,
                                           role_formation_metier=role_formation_metier,
                                           user=user
                                           )


def create_test_seance(formation, seance_date, local, participant_max_number, formateur, duree):
    return Seance.objects.create(formation=formation,
                                 seance_date=seance_date,
                                 local=local,
                                 participant_max_number=participant_max_number,
                                 formateur=formateur,
                                 duree=duree
                                 )


def create_test_register(seance, participant):
    return Register.objects.create(seance=seance,
                                   participant=participant
                                   )


def create_test_formation(code, name, public_cible):
    return Formation.objects.create(code=code,
                                    name=name,
                                    description="description de test",
                                    public_cible=public_cible, )


def create_test_user(username, password):
    return User.objects.create(username=username, password=password)
