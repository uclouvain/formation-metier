from django.contrib.auth.models import Permission, User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from formation_metier.enums.roles_osis_enum import ROLES_OSIS_CHOICES
from formation_metier.models.formation import Formation
from formation_metier.tests.utils import create_test_formation, create_test_user

URL_NEW_FORMATION_VIEW = reverse('formation_metier:new_formation')
FORMATION_DESCRIPTION = "formation de test"


class NewFormationFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.formation1 = create_test_formation(name="formation_test_1", code="AAAA01",
                                               public_cible=ROLES_OSIS_CHOICES[1])
        cls.user1 = create_test_user(username="user1", password="password123")
        cls.user1.user_permissions.add(
            Permission.objects.get(codename='access_to_formation_fare'))
        cls.user1.user_permissions.add(
            Permission.objects.get(codename='add_formation'))
        cls.user1 = User.objects.get(pk=cls.user1.pk)

    def test_should_authorise_access_to_formateur(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(URL_NEW_FORMATION_VIEW)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h2>Nouvelle formation</h2>", html=True)

    def test_should_deny_access_user_case_not_logged(self):
        response = self.client.get(URL_NEW_FORMATION_VIEW)
        self.assertEqual(response.status_code, 302)

    def test_should_deny_access_case_user_not_have_permission_add_formateur(self):
        user2 = create_test_user(username="user2", password="password123")
        user2.user_permissions.add(Permission.objects.get(codename='add_formation'))
        user2 = User.objects.get(pk=user2.pk)
        self.client.force_login(user=user2)
        response = self.client.get(URL_NEW_FORMATION_VIEW)
        self.assertEqual(response.status_code, 403)

    def test_should_deny_access_case_user_not_have_permission_access_to_formation_fare(self):
        user2 = create_test_user(username="user2", password="password123")
        user2.user_permissions.add(Permission.objects.get(codename='access_to_formation_fare'))
        user2 = User.objects.get(pk=user2.pk)
        self.client.force_login(user=user2)
        response = self.client.get(URL_NEW_FORMATION_VIEW)
        self.assertEqual(response.status_code, 403)

    def test_should_not_raise_exception(self):
        self.client.force_login(user=self.user1)
        data = {"name": "formation_test_2",
                "code": "AAAA02",
                "description": FORMATION_DESCRIPTION,
                'public_cible': ROLES_OSIS_CHOICES[1]}
        response = self.client.post(URL_NEW_FORMATION_VIEW, data=data)
        self.assertEqual(response.status_code, 200)

    def test_should_raise_validation_error_case_code_already_exist(self):
        self.client.force_login(user=self.user1)
        data = {"name": "formation_test_2",
                "code": "AAAA01",
                "description": FORMATION_DESCRIPTION,
                'public_cible': ROLES_OSIS_CHOICES[1]}
        response = self.client.get(URL_NEW_FORMATION_VIEW)
        request = self.client.post(URL_NEW_FORMATION_VIEW, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 200)
        self.assertRaisesMessage(ValidationError,
                                 "Un objet Formation avec ce champ Code existe déjà.")
        self.assertFormError(request, 'form', "code", ["Un objet Formation avec ce champ Code existe déjà."])

    def test_should_raise_validation_error_case_code_format(self):
        self.client.force_login(user=self.user1)
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
        self.client.force_login(user=self.user1)
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
