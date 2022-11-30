import factory
import factory.fuzzy

from formation_metier.tests.factories.employe_uclouvain import EmployeUCLouvainFormateurFactory
from formation_metier.tests.factories.formation import FormationFactory


class SeanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'formation_metier.Seance'

    formation = factory.SubFactory(FormationFactory)
    seance_date = factory.fuzzy.FuzzyDate(start_date=(2022, 1, 1), end_date=(2024, 12, 31))
    local = factory.fuzzy.FuzzyText(length=7)
    participant_max_number = factory.fuzzy
    formateur = factory.SubFactory(EmployeUCLouvainFormateurFactory)
    duree = factory.fuzzy.FuzzyInteger(1, 599)
