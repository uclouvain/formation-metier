from formation_metier.models.formation import Formation
from formation_metier.models.participant import Participant
from formation_metier.models.formateur import Formateur
from formation_metier.models.session import Session
from formation_metier.models.register import Register
from formation_metier.models.person import Person


def create_test_person(name, number_fgs, role_formation_metier):
    return Person.objects.create(name=name,
                                 numberFGS=number_fgs,
                                 role_formation_metier=role_formation_metier
                                 )


def create_test_participant(person):
    return Participant.objects.create(person=person)


def create_test_formateur(person):
    return Formateur.objects.create(person=person)


def create_test_session(formation, session_date, local, participant_max_number, formateur, public_cible):
    return Session.objects.create(formation=formation,
                                  session_date=session_date,
                                  local=local,
                                  participant_max_number=participant_max_number,
                                  formateur=formateur,
                                  public_cible=public_cible
                                  )


def create_test_register(session, participant, register_date):
    return Register.objects.create(session=session,
                                   participant=participant,
                                   register_date=register_date
                                   )


def create_test_formation(code, name):
    return Formation.objects.create(code=code,
                                    name=name,
                                    description="description de test")
