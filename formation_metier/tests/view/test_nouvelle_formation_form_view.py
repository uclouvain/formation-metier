from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from formation_metier.enums.roles_osis_enum import ROLES_OSIS_CHOICES
from formation_metier.models.formation import Formation
from formation_metier.tests.factories.employe_uclouvain import EmployeUCLouvainWithPermissionsFactory
from formation_metier.tests.factories.formation import FormationFactory

URL_NEW_FORMATION_VIEW = reverse('formation_metier:nouvelle_formation')
FORMATION_DESCRIPTION = "formation de test"


class NouvelleFormationFormViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.employe_ucl = EmployeUCLouvainWithPermissionsFactory('access_to_formation_fare', 'add_formation')
        cls.formation = FormationFactory()

    def test_should_authorise_access_to_formateur(self):
        self.client.force_login(user=self.employe_ucl.user)
        response = self.client.get(URL_NEW_FORMATION_VIEW)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h2>Nouvelle formation</h2>", html=True)

    def test_should_deny_access_user_case_not_logged(self):
        response = self.client.get(URL_NEW_FORMATION_VIEW)
        self.assertEqual(response.status_code, 302)

    def test_should_deny_access_case_user_not_have_permission_add_formateur(self):
        employe_ucl = EmployeUCLouvainWithPermissionsFactory('access_to_formation_fare')
        self.client.force_login(user=employe_ucl.user)
        response = self.client.get(URL_NEW_FORMATION_VIEW)
        self.assertEqual(response.status_code, 403)

    def test_should_deny_access_case_user_not_have_permission_access_to_formation_fare(self):
        employe_ucl = EmployeUCLouvainWithPermissionsFactory('add_formation')
        self.client.force_login(user=employe_ucl.user)
        response = self.client.get(URL_NEW_FORMATION_VIEW)
        self.assertEqual(response.status_code, 403)

    def test_should_not_raise_exception(self):
        self.client.force_login(user=self.employe_ucl.user)
        data = {"name": "formation_test_2",
                "code": "AAAA02",
                "description": FORMATION_DESCRIPTION,
                'public_cible': ROLES_OSIS_CHOICES[1]}
        response = self.client.post(URL_NEW_FORMATION_VIEW, data=data)
        self.assertEqual(response.status_code, 200)

    def test_should_raise_validation_error_case_code_already_exist(self):
        self.client.force_login(user=self.employe_ucl.user)
        data = {"name": "formation_test_2",
                "code": self.formation.code,
                "description": FORMATION_DESCRIPTION,
                'public_cible': ROLES_OSIS_CHOICES[1]}
        response = self.client.get(URL_NEW_FORMATION_VIEW)
        request = self.client.post(URL_NEW_FORMATION_VIEW, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Formation.objects.count(), 1)
        self.assertRaisesMessage(ValidationError,
                                 "Un objet Formation avec ce champ Code existe déjà.")
        self.assertFormError(request, 'form', "code", ["Un objet Formation avec ce champ Code existe déjà."])

    def test_should_raise_validation_error_case_code_format(self):
        self.client.force_login(user=self.employe_ucl.user)
        data = {"name": "Fromation_test_2",
                "code": "AAAA01A",
                "description": FORMATION_DESCRIPTION,
                'public_cible': ROLES_OSIS_CHOICES[1]}
        response = self.client.get(URL_NEW_FORMATION_VIEW)
        request = self.client.post(URL_NEW_FORMATION_VIEW, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Formation.objects.count(), 1)
        self.assertFormError(request,
                             'form',
                             "code",
                             [
                                 f'Assurez-vous que cette valeur comporte au plus 6 caractères (actuellement {len(data["code"])}).'])

    def test_should_raise_validation_error_case_code_length(self):
        self.client.force_login(user=self.employe_ucl.user)
        data = {"name": "Fromation_test_2",
                "code": "AAA001",
                "description": FORMATION_DESCRIPTION,
                'public_cible': ROLES_OSIS_CHOICES[1]}
        response = self.client.get(URL_NEW_FORMATION_VIEW)
        request = self.client.post(URL_NEW_FORMATION_VIEW, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Formation.objects.count(), 1)
        self.assertFormError(request, 'form', "code",
                             ['Saisissez une valeur valide.'])
