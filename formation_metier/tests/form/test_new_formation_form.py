from datetime import datetime

from django.contrib.auth.models import Permission, User
from django.core.exceptions import ValidationError
from django.test import TestCase

from django.urls import reverse

from formation_metier.enums.roles_osis_enum import ROLES_OSIS_CHOICES
from formation_metier.models.formation import Formation
from formation_metier.tests.utils import create_test_formation, create_test_user

URL_NEW_FORMATION_VIEW = reverse('formation_metier:new_formation')


class NewFormationFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.formation1 = create_test_formation(name="formation_test_1", code="AAAA01",
                                               public_cible=ROLES_OSIS_CHOICES[1])
        cls.user1 = create_test_user(username="user1", password="password123")
        cls.user2 = create_test_user(username="user2", password="password123")
        cls.user3 = create_test_user(username="user3", password="password123")
        cls.user1.user_permissions.add(
            Permission.objects.get(codename='access_to_formation_fare'))
        cls.user1.user_permissions.add(
            Permission.objects.get(codename='add_formation'))
        cls.user2.user_permissions.add(
            Permission.objects.get(codename='add_formation'))
        cls.user3.user_permissions.add(
            Permission.objects.get(codename='access_to_formation_fare'))
        cls.user1 = User.objects.get(pk=cls.user1.pk)
        cls.user2 = User.objects.get(pk=cls.user2.pk)
        cls.user3 = User.objects.get(pk=cls.user3.pk)

    def test_get(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(URL_NEW_FORMATION_VIEW)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h2>Nouvelle formation</h2>", html=True)

    def test_get_without_force_login(self):
        response = self.client.get(URL_NEW_FORMATION_VIEW)
        self.assertEqual(response.status_code, 302)

    def test_get_without_permission_access_to_formation_fare(self):
        self.client.force_login(user=self.user2)
        response = self.client.get(URL_NEW_FORMATION_VIEW)
        self.assertEqual(response.status_code, 403)

    def test_get_without_permission_add_formation(self):
        self.client.force_login(user=self.user3)
        response = self.client.get(URL_NEW_FORMATION_VIEW)
        self.assertEqual(response.status_code, 403)

    def test_with_valid_data_and_respected_constaint(self):
        self.client.force_login(user=self.user1)
        data = {"name": "formation_test_2",
                "code": "AAAA02",
                "description": "formation de test",
                'public_cible': ROLES_OSIS_CHOICES[1]}
        response = self.client.post(URL_NEW_FORMATION_VIEW, data=data)
        self.assertEqual(response.status_code, 200)

    def test_with_valid_data_and_unrespected_constaint(self):
        self.client.force_login(user=self.user1)
        data = {"name": "formation_test_2",
                "code": "AAAA01",
                "description": "formation de test",
                'public_cible': ROLES_OSIS_CHOICES[1]}
        response = self.client.get(URL_NEW_FORMATION_VIEW)
        request = self.client.post(URL_NEW_FORMATION_VIEW, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 200)
        self.assertRaisesMessage(ValidationError,
                                 "Un objet Formation avec ce champ Code existe déjà.")
        self.assertFormError(request, 'form', "code", ["Un objet Formation avec ce champ Code existe déjà."])

    # a faire si CharFiled ne convertis pas automatiquement en str
    def test_with_invalid_data_name(self):
        self.client.force_login(user=self.user1)
        data = {"name": True,
                "code": "AAAA01",
                "description": "formation de test",
                'public_cible': ROLES_OSIS_CHOICES[1]}
        response = self.client.get(URL_NEW_FORMATION_VIEW)
        request = self.client.post(URL_NEW_FORMATION_VIEW, data=data)

        self.assertEqual(response.status_code, 200)
        # self.assertEqual(request.status_code, 200)
        # self.assertEqual(Formation.objects.count(), 1)
        # self.assertFormError(request, 'form', "name", ["Un objet Formation avec ce champ Code existe déjà."])

    def test_with_invalid_data_code_length(self):
        self.client.force_login(user=self.user1)
        data = {"name": "Fromation_test_2",
                "code": "AAAA01A",
                "description": "formation de test",
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

    def test_with_invalid_data_code_format(self):
        self.client.force_login(user=self.user1)
        data = {"name": "Fromation_test_2",
                "code": "AAA001",
                "description": "formation de test",
                'public_cible': ROLES_OSIS_CHOICES[1]}
        response = self.client.get(URL_NEW_FORMATION_VIEW)
        request = self.client.post(URL_NEW_FORMATION_VIEW, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Formation.objects.count(), 1)
        self.assertFormError(request, 'form', "code",
                             ['Saisissez une valeur valide.'])

    # a faire si CharFiled ne convertis pas automatiquement en str
    def test_with_invalid_data_description(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(URL_NEW_FORMATION_VIEW)
