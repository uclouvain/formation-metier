import random
import string

import factory
import factory.fuzzy
from formation_metier.enums.roles_osis_enum import ROLES_OSIS_CHOICES


def generate_code_formation() -> str:
    text_code = [random.choice(string.ascii_uppercase) for _ in range(4)]
    digit_code = [random.choice(string.digits) for _ in range(2)]
    return "".join(text_code + digit_code)


class FormationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'formation_metier.Formation'

    code = factory.LazyFunction(generate_code_formation)
    name = factory.Faker('name')
    description = factory.fuzzy.FuzzyText(length=70)
    public_cible = factory.fuzzy.FuzzyChoice(ROLES_OSIS_CHOICES)
