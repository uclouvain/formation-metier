from unittest import TestCase

from formation_metier.enums.roles_osis_enum import ROLES_OSIS_CHOICES
from formation_metier.forms.nouvelle_formation_form import NouvelleFormationForm
from formation_metier.tests.factories.employe_uclouvain import EmployeUCLouvainWithPermissionsFactory


class NouvelleFormationFormViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.employe_ucl = EmployeUCLouvainWithPermissionsFactory('access_to_formation_fare', 'add_formation')

    def test_valid_form(self):
        data = {
            'code': "AAAA11",
            'name': "test_from",
            'description': "Test du formulaire",
            'public_cible': ROLES_OSIS_CHOICES[0],
        }
        form = NouvelleFormationForm(data=data)
        self.assertTrue(form.is_valid())
