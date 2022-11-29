from django.contrib.auth.models import Permission, User
from django.db.utils import IntegrityError
from django.test import TestCase
from datetime import datetime

from django.urls import reverse
from django.core.exceptions import ValidationError

from formation_metier.enums.roles_osis_enum import ROLES_OSIS_CHOICES
from formation_metier.models.employe_uclouvain import RoleFormationFareEnum
from formation_metier.models.register import Register
from formation_metier.tests.utils import create_test_formation, create_test_seance, \
    create_test_register, create_test_user, create_test_employe_ucl

URL_NEW_REGISTRATION = 'formation_metier:detail_seance'


class NewRegisterFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.date = datetime.today()
        cls.user1 = create_test_user(username="user1", password="password123")
        cls.user2 = create_test_user(username="user2", password="password123")
        cls.user1.user_permissions.add(
            Permission.objects.get(codename='access_to_formation_fare'))
        cls.user1.user_permissions.add(
            Permission.objects.get(codename='view_register'))
        cls.user1.user_permissions.add(
            Permission.objects.get(codename='add_register'))
        cls.user1.user_permissions.add(
            Permission.objects.get(codename='view_seance'))

        cls.user1 = User.objects.get(pk=cls.user1.pk)
        cls.formation1 = create_test_formation(name="formation_test_1", code="AAAAA0001",
                                               public_cible=ROLES_OSIS_CHOICES[1])

        cls.employe_ucl1 = create_test_employe_ucl(name="Formateur1",
                                                   number_fgs="AAA01",
                                                   role_formation_metier=RoleFormationFareEnum.FORMATEUR,
                                                   user=cls.user1)
        cls.employe_ucl2 = create_test_employe_ucl(name="Participant1",
                                                   number_fgs="AAA02",
                                                   role_formation_metier=RoleFormationFareEnum.PARTICIPANT,
                                                   user=cls.user2)

        cls.seance1 = create_test_seance(formation=cls.formation1,
                                         seance_date=cls.date,
                                         participant_max_number=2,
                                         local="L001",
                                         formateur=cls.employe_ucl1,
                                         duree=60
                                         )
        cls.register1 = create_test_register(seance=cls.seance1, participant=cls.employe_ucl2)

    def test_should_authorise_access_to_formateur(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"<h2>Formation : {self.formation1.name}</h2>", html=True)
        self.assertTemplateUsed('detail_seance.html')

    def test_should_deny_access_user_case_not_logged(self):
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]))
        self.assertEqual(response.status_code, 302)

    def test_should_deny_access_case_user_not_have_permission_access_to_formation_fare(self):
        user3 = create_test_user(username="user3", password="password123")
        user3.user_permissions.add(Permission.objects.get(codename='add_register'))
        user3.user_permissions.add(Permission.objects.get(codename='view_register'))
        user3.user_permissions.add(Permission.objects.get(codename='view_seance'))
        user2 = User.objects.get(pk=user3.pk)
        self.client.force_login(user=user3)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]))
        self.assertEqual(response.status_code, 403)

    def test_should_deny_access_case_user_not_have_permission_add_register(self):
        user3 = create_test_user(username="user3", password="password123")
        user3.user_permissions.add(Permission.objects.get(codename='access_to_formation_fare'))
        user3.user_permissions.add(Permission.objects.get(codename='view_register'))
        user3.user_permissions.add(Permission.objects.get(codename='view_seance'))
        user3 = User.objects.get(pk=user3.pk)
        employe_ucl3 = create_test_employe_ucl(name="Participant1",
                                               number_fgs="AAA03",
                                               role_formation_metier=RoleFormationFareEnum.PARTICIPANT,
                                               user=user3)
        self.client.force_login(user=user3)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]))
        self.assertEqual(response.status_code, 200)
        data = {"seance": self.seance1,
                "participant": employe_ucl3.id
                }
        request = self.client.post(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]), data=data)
        self.assertEqual(request.status_code, 403)

    def test_should_deny_access_case_user_not_have_permission_view_seance(self):
        user3 = create_test_user(username="user3", password="password123")
        user3.user_permissions.add(Permission.objects.get(codename='access_to_formation_fare'))
        user3.user_permissions.add(Permission.objects.get(codename='view_register'))
        user3.user_permissions.add(Permission.objects.get(codename='add_register'))
        user3 = User.objects.get(pk=user3.pk)
        self.client.force_login(user=user3)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]))
        self.assertEqual(response.status_code, 403)

    def test_should_deny_access_case_user_not_have_permission_view_register(self):
        user3 = create_test_user(username="user3", password="password123")
        user3.user_permissions.add(Permission.objects.get(codename='access_to_formation_fare'))
        user3.user_permissions.add(Permission.objects.get(codename='view_seance'))
        user3.user_permissions.add(Permission.objects.get(codename='add_register'))
        user3 = User.objects.get(pk=user3.pk)
        self.client.force_login(user=user3)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]))
        self.assertEqual(response.status_code, 403)

    def test_should_not_raise_exception(self):
        user3 = create_test_user(username="user3", password="password123")
        employe_ucl3 = create_test_employe_ucl(name="Participant1",
                                               number_fgs="AAA03",
                                               role_formation_metier=RoleFormationFareEnum.PARTICIPANT,
                                               user=user3)
        self.client.force_login(user=self.user1)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]))
        data = {"seance": self.seance1,
                "participant": employe_ucl3.id
                }

        request = self.client.post(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 302)
        self.assertEqual(Register.objects.count(), 2)

    def test_should_raise_validation_error_case_register_already_exist(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]))
        data = {"seance": self.seance1,
                "participant": self.employe_ucl2.id
                }

        request = self.client.post(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Register.objects.count(), 1)
        self.assertRaisesMessage(ValidationError,
                                 f"L'utilisateur {self.employe_ucl2} est déja inscit à cette formation")

    def test_should_raise_validation_error_case_sceance_max_participant_number(self):
        user3 = create_test_user(username="user3", password="password123")
        user4 = create_test_user(username="user4", password="password123")
        employe_ucl3 = create_test_employe_ucl(name="Participant2",
                                               number_fgs="AAA03",
                                               role_formation_metier=RoleFormationFareEnum.PARTICIPANT,
                                               user=user3)
        employe_ucl4 = create_test_employe_ucl(name="Participant3",
                                               number_fgs="AAA04",
                                               role_formation_metier=RoleFormationFareEnum.PARTICIPANT,
                                               user=user4)
        self.client.force_login(user=self.user1)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]))
        data1 = {"seance": self.seance1,
                 "participant": employe_ucl3.id
                 }

        data2 = {"seance": self.seance1,
                 "participant": employe_ucl4.id
                 }
        self.assertEqual(response.status_code, 200)
        first_request = self.client.post(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]), data=data1)
        self.assertEqual(first_request.status_code, 302)
        second_request = self.client.post(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]), data=data2)
        self.assertEqual(second_request.status_code, 200)
        self.assertEqual(Register.objects.count(), 2)
        self.assertRaisesMessage(ValidationError,
                                 'Le nombre maximal de participant inscit a cette seance est déjà atteint')

    def test_should_raise_validation_error_case_sceance_not_exist(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]))
        data = {"seance": "test",
                "participant": 19
                }

        request = self.client.post(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Register.objects.count(), 1)
        self.assertRaises(ValueError)
