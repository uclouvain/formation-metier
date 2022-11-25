from datetime import datetime
from pprint import pprint

from django.contrib.auth.models import Permission, User
from django.core.exceptions import ValidationError
from django.test import TestCase

from django.urls import reverse
from formation_metier.models.person import Person, RoleFormationFareEnum
from formation_metier.models.session import Session
from formation_metier.tests.utils import create_test_formation, create_test_session, create_test_person, \
    create_test_formateur, create_test_user
from formation_metier.enums.roles_osis_enum import ROLES_OSIS_CHOICES

URL_NEW_SESSION_VIEW = 'formation_metier:new_session'


class NewSessionFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.date = datetime.today()
        cls.user1 = create_test_user(username="user1", password="password123")
        cls.user2 = create_test_user(username="user2", password="password123")
        cls.user3 = create_test_user(username="user3", password="password123")
        cls.user1.user_permissions.add(
            Permission.objects.get(codename='access_to_formation_fare'))
        # pk=29 => Permission : 'formation_metier.add_session'
        cls.user1.user_permissions.add(
            Permission.objects.get(pk=29))
        cls.user2.user_permissions.add(
            Permission.objects.get(pk=29))
        cls.user3.user_permissions.add(
            Permission.objects.get(codename='access_to_formation_fare'))
        cls.user1 = User.objects.get(pk=cls.user1.pk)

        cls.user2 = User.objects.get(pk=cls.user2.pk)
        cls.user3 = User.objects.get(pk=cls.user3.pk)

        cls.formation1 = create_test_formation(name="formation_test_1", code="AAAAA0001")
        cls.person1 = create_test_person(name="test", number_fgs="AAA01",
                                         role_formation_metier=RoleFormationFareEnum.PARTICIPANT)
        cls.formateur1 = create_test_formateur(person=cls.person1)
        cls.session1 = create_test_session(formation=cls.formation1,
                                           session_date=cls.date,
                                           participant_max_number=10,
                                           local="L001",
                                           formateur=cls.formateur1,
                                           public_cible=ROLES_OSIS_CHOICES[1],
                                           duree=60
                                           )

    def test_get(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h2>Nouvelle session</h2>", html=True)
        self.assertTemplateUsed('new_session.html')

    def test_get_without_force_login(self):
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]))
        self.assertEqual(response.status_code, 302)

    def test_get_without_permission_access_to_formation_fare(self):
        self.client.force_login(user=self.user2)
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]))
        self.assertEqual(response.status_code, 403)

    def test_get_without_permission_add_formation(self):
        self.client.force_login(user=self.user3)
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]))
        self.assertEqual(response.status_code, 403)

    def test_with_valid_data_and_respected_constaint(self):
        self.client.force_login(user=self.user1)
        data = {"formation": self.formation1,
                "session_date": self.date,
                "participant_max_number": 10,
                "local": "L002",
                "formateur": self.formateur1,
                "public_cible": ROLES_OSIS_CHOICES[1],
                "duree": 20
                }
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]))
        self.assertEqual(response.status_code, 200)
        request = self.client.post(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]), data=data)
        Session.objects.create(formation=self.formation1,
                               session_date=self.date,
                               participant_max_number=10,
                               local="L002",
                               formateur=self.formateur1,
                               public_cible=ROLES_OSIS_CHOICES[1],
                               duree=20)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Session.objects.count(), 2)

    def test_with_invalid_data_formation(self):
        self.client.force_login(user=self.user1)
        data = {"formation": "test",
                "session_date": self.date,
                "participant_max_number": 10,
                "local": "L001",
                "formateur": self.formateur1,
                "public_cible": ROLES_OSIS_CHOICES[1],
                'duree': 700}
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]))
        request = self.client.post(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Session.objects.count(), 1)
        self.assertRaisesMessage(ValidationError,
                                 'Un objet Session avec ces champs Session date, Local et Formateur existe déjà.')
        self.assertRaisesMessage(ValidationError,
                                 'Assurez-vous que cette valeur est inférieure ou égale à 600.')
