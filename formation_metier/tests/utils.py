from django.contrib.auth.models import User

from formation_metier.models.formation import Formation
from formation_metier.models.participant import Participant
from formation_metier.models.formateur import Formateur
from formation_metier.models.session import Session
from formation_metier.models.register import Register
from formation_metier.models.person import Person


def create_test_person(name, number_fgs, role_formation_metier, user=None):
    return Person.objects.create(name=name,
                                 numberFGS=number_fgs,
                                 role_formation_metier=role_formation_metier,
                                 user=user
                                 )


def create_test_participant(person):
    return Participant.objects.create(person=person)


def create_test_formateur(person):
    return Formateur.objects.create(person=person)


def create_test_session(formation, session_date, local, participant_max_number, formateur, public_cible, duree):
    return Session.objects.create(formation=formation,
                                  session_date=session_date,
                                  local=local,
                                  participant_max_number=participant_max_number,
                                  formateur=formateur,
                                  public_cible=public_cible,
                                  duree=duree
                                  )


def create_test_register(session, participant):
    return Register.objects.create(session=session,
                                   participant=participant
                                   )


def create_test_formation(code, name):
    return Formation.objects.create(code=code,
                                    name=name,
                                    description="description de test")


def create_test_user(username, password):
    return User.objects.create(username=username, password=password)
