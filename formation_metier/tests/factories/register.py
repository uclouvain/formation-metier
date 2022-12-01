import factory

from formation_metier.tests.factories.employe_uclouvain import EmployeUCLouvainParticipantFactory
from formation_metier.tests.factories.seance import SeanceFactory


class RegisterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'formation_metier.Register'

    seance = factory.SubFactory(SeanceFactory)
    participant = factory.SubFactory(EmployeUCLouvainParticipantFactory)
