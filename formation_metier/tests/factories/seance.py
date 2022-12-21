import datetime

import factory.fuzzy

from formation_metier.tests.factories.employe_uclouvain import EmployeUCLouvainFormateurFactory
from formation_metier.tests.factories.formation import FormationFactory


class SeanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'formation_metier.Seance'

    formation = factory.SubFactory(FormationFactory)
    seance_date = factory.fuzzy.FuzzyDate(start_date=datetime.date(2022, 1, 1))
    local = factory.fuzzy.FuzzyText(length=7)
    participant_max_number = factory.fuzzy.FuzzyInteger(1, 100)
    formateur = factory.SubFactory(EmployeUCLouvainFormateurFactory)
    duree = factory.fuzzy.FuzzyInteger(1, 599)


class SeanceForExistingFormationFactory:
    def __init__(self, existing_formation, **kwargs):
        self.seance = SeanceFactory(**kwargs)
        self.seance.formation = existing_formation
        existing_formation.seance_set.add(self.seance)

    def __new__(cls, existing_formation, **kwargs):
        obj = super().__new__(cls)
        obj.__init__(existing_formation, **kwargs)
        return obj.seance
