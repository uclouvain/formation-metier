import factory

from formation_metier.tests.factories.employe_uclouvain import EmployeUCLouvainParticipantFactory
from formation_metier.tests.factories.seance import SeanceFactory


class InscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'formation_metier.Inscription'

    seance = factory.SubFactory(SeanceFactory)
    participant = factory.SubFactory(EmployeUCLouvainParticipantFactory)
