from datetime import datetime
from pprint import pprint

from django.contrib.auth.models import Permission, User
from django.core.exceptions import ValidationError
from django.test import TestCase

from django.urls import reverse
from formation_metier.models.employe_uclouvain import EmployeUCLouvain, RoleFormationFareEnum
from formation_metier.models.seance import Seance
from formation_metier.tests.utils import create_test_formation, create_test_seance, create_test_employe_ucl, \
    create_test_user
from formation_metier.enums.roles_osis_enum import ROLES_OSIS_CHOICES

URL_NEW_SESSION_VIEW = 'formation_metier:new_seance'


class NewSessionFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.date = datetime.today()
        cls.user1 = create_test_user(username="user1", password="password123")
        cls.user1.user_permissions.add(
            Permission.objects.get(codename='access_to_formation_fare'))
        # pk=29 => Permission : 'formation_metier.add_session'
        cls.user1.user_permissions.add(
            Permission.objects.get(codename='add_seance'))
        cls.user1 = User.objects.get(pk=cls.user1.pk)
        cls.formation1 = create_test_formation(name="formation_test_1", code="AAAAA0001",
                                               public_cible=ROLES_OSIS_CHOICES[1])
        cls.employe_ucl1 = create_test_employe_ucl(name="test", number_fgs="AAA01",
                                                   role_formation_metier=RoleFormationFareEnum.FORMATEUR,
                                                   user=cls.user1)
        cls.session1 = create_test_seance(formation=cls.formation1,
                                          seance_date=cls.date,
                                          participant_max_number=10,
                                          local="L001",
                                          formateur=cls.employe_ucl1,
                                          duree=60
                                          )

    def test_should_authorise_access_to_formateur(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h2>Nouvelle séance</h2>", html=True)
        self.assertTemplateUsed('new_session.html')

    def test_should_deny_access_case_user_not_logged(self):
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]))
        self.assertEqual(response.status_code, 302)

    def test_should_deny_access_case_user_not_have_permission_access_to_formation_fare(self):
        user2 = create_test_user(username="user2", password="password123")
        user2.user_permissions.add(Permission.objects.get(codename='add_seance'))
        user2 = User.objects.get(pk=user2.pk)
        self.client.force_login(user=user2)
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]))
        self.assertEqual(response.status_code, 403)

    def test_should_deny_access_case_user_not_have_permission_add_seance(self):
        user2 = create_test_user(username="user2", password="password123")
        user2.user_permissions.add(Permission.objects.get(codename='access_to_formation_fare'))
        user2 = User.objects.get(pk=user2.pk)
        self.client.force_login(user=user2)
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]))
        self.assertEqual(response.status_code, 403)

    def test_should_not_raise_exception(self):
        self.client.force_login(user=self.user1)
        data = {"formation": self.formation1,
                "seance_date": self.date,
                "participant_max_number": 10,
                "local": "L002",
                "formateur": self.employe_ucl1,
                "duree": 20
                }
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]))
        self.assertEqual(response.status_code, 200)
        request = self.client.post(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]), data=data)
        Seance.objects.create(formation=self.formation1,
                              seance_date=self.date,
                              participant_max_number=10,
                              local="L002",
                              formateur=self.employe_ucl1,
                              duree=20)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Seance.objects.count(), 2)

    def test_should_raise_validation_error_case_code_date_formateur_already_exist(self):
        self.client.force_login(user=self.user1)
        data = {"formation": "test",
                "seance_date": self.date,
                "participant_max_number": 10,
                "local": "L001",
                "formateur": self.employe_ucl1,
                'duree': 60}
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]))
        request = self.client.post(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Seance.objects.count(), 1)
        self.assertRaisesMessage(ValidationError,
                                 'Un objet Seance avec ces champs Seance date, Local et Formateur existe déjà.')

    def test_should_raise_validation_error_case_duree_value(self):
        self.client.force_login(user=self.user1)
        data = {"formation": "test",
                "seance_date": self.date,
                "participant_max_number": 10,
                "local": "L001",
                "formateur": self.employe_ucl1,
                'duree': 700}
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]))
        request = self.client.post(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Seance.objects.count(), 1)
        self.assertRaisesMessage(ValidationError,
                                 'Assurez-vous que cette valeur est inférieure ou égale à 600.')
