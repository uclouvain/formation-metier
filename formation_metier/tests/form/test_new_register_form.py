from django.contrib.auth.models import Permission, User
from django.test import TestCase
from datetime import datetime

from django.urls import reverse
from django.core.exceptions import ValidationError

from formation_metier.enums.roles_osis_enum import ROLES_OSIS_CHOICES
from formation_metier.models.employe_uclouvain import EmployeUCLouvain, RoleFormationFareEnum
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
        cls.user3 = create_test_user(username="user3", password="password123")
        cls.user4 = create_test_user(username="user4", password="password123")
        cls.user5 = create_test_user(username="user5", password="password123")
        cls.user6 = create_test_user(username="user6", password="password123")
        cls.user7 = create_test_user(username="user7", password="password123")
        cls.user1.user_permissions.add(
            Permission.objects.get(codename='access_to_formation_fare'))
        cls.user1.user_permissions.add(
            Permission.objects.get(codename='view_register'))
        cls.user1.user_permissions.add(
            Permission.objects.get(codename='add_register'))
        cls.user1.user_permissions.add(
            Permission.objects.get(codename='view_seance'))
        cls.user2.user_permissions.add(
            Permission.objects.get(codename='access_to_formation_fare'))
        cls.user2.user_permissions.add(
            Permission.objects.get(codename='view_seance'))

        cls.user3.user_permissions.add(
            Permission.objects.get(codename='access_to_formation_fare'))
        cls.user3.user_permissions.add(
            Permission.objects.get(codename='view_register'))

        cls.user4.user_permissions.add(
            Permission.objects.get(codename='view_seance'))
        cls.user4.user_permissions.add(
            Permission.objects.get(codename='view_register'))

        cls.user1 = User.objects.get(pk=cls.user1.pk)
        cls.user2 = User.objects.get(pk=cls.user2.pk)
        cls.user3 = User.objects.get(pk=cls.user3.pk)
        cls.user4 = User.objects.get(pk=cls.user4.pk)
        cls.formation1 = create_test_formation(name="formation_test_1", code="AAAAA0001",
                                               public_cible=ROLES_OSIS_CHOICES[1])

        cls.employe_ucl1 = create_test_employe_ucl(name="Formateur1",
                                              number_fgs="AAA01",
                                              role_formation_metier=RoleFormationFareEnum.FORMATEUR, user=cls.user1)
        cls.employe_ucl2 = create_test_employe_ucl(name="Participant1",
                                              number_fgs="AAA02",
                                              role_formation_metier=RoleFormationFareEnum.PARTICIPANT, user=cls.user2)
        cls.employe_ucl3 = create_test_employe_ucl(name="Participant2",
                                              number_fgs="AAA03",
                                              role_formation_metier=RoleFormationFareEnum.PARTICIPANT, user=cls.user3)
        cls.employe_ucl4 = create_test_employe_ucl(name="Participant3",
                                              number_fgs="AAA04",
                                              role_formation_metier=RoleFormationFareEnum.PARTICIPANT, user=cls.user4)
        cls.employe_ucl5 = create_test_employe_ucl(name="Participant4",
                                              number_fgs="AAA05",
                                              role_formation_metier=RoleFormationFareEnum.PARTICIPANT, user=cls.user5)
        cls.employe_ucl6 = create_test_employe_ucl(name="Participant5",
                                              number_fgs="AAA06",
                                              role_formation_metier=RoleFormationFareEnum.PARTICIPANT, user=cls.user6)
        cls.employe_ucl7 = create_test_employe_ucl(name="Participant6",
                                              number_fgs="AAA07",
                                              role_formation_metier=RoleFormationFareEnum.PARTICIPANT, user=cls.user7)

        cls.seance1 = create_test_seance(formation=cls.formation1,
                                         seance_date=cls.date,
                                         participant_max_number=5,
                                         local="L001",
                                         formateur=cls.employe_ucl1,
                                         duree=60
                                         )

        cls.register1 = create_test_register(seance=cls.seance1, participant=cls.employe_ucl2)
        cls.register2 = create_test_register(seance=cls.seance1, participant=cls.employe_ucl3)
        cls.register3 = create_test_register(seance=cls.seance1, participant=cls.employe_ucl4)
        cls.register4 = create_test_register(seance=cls.seance1, participant=cls.employe_ucl5)

    def test_get(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"<h2>Formation : {self.formation1.name}</h2>", html=True)
        self.assertTemplateUsed('detail_seance.html')

    def test_get_without_force_login(self):
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]))
        self.assertEqual(response.status_code, 302)

    def test_get_without_permission_access_to_formation_fare(self):
        self.client.force_login(user=self.user4)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]))
        self.assertEqual(response.status_code, 403)

    def test_get_without_permission_view_seance(self):
        self.client.force_login(user=self.user3)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]))
        self.assertEqual(response.status_code, 403)

    def test_get_without_permission_view_register(self):
        self.client.force_login(user=self.user2)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]))
        self.assertEqual(response.status_code, 403)

    def test_with_valid_data_and_respected_constaint(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]))
        data = {"seance": self.seance1,
                "participant": self.employe_ucl6.id
                }

        request = self.client.post(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 302)
        self.assertEqual(Register.objects.count(), 5)

    def test_with_valid_data_and_unrespected_constaint_existing_register(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]))
        data = {"seance": self.seance1,
                "participant": self.employe_ucl5.id
                }

        request = self.client.post(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Register.objects.count(), 4)
        self.assertRaisesMessage(ValidationError,
                                 'Un objet Register avec ces champs Seance et Participant existe déjà.')

    def test_with_valid_data_and_unrespected_constaint_number_max(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]))
        data1 = {"seance": self.seance1,
                 "participant": self.employe_ucl6.id
                 }

        data2 = {"seance": self.seance1,
                 "participant": self.employe_ucl7.id
                 }

        self.assertEqual(response.status_code, 200)
        first_request = self.client.post(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]), data=data1)
        self.assertEqual(first_request.status_code, 302)
        second_request = self.client.post(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]), data=data2)
        self.assertEqual(second_request.status_code, 200)
        self.assertEqual(Register.objects.count(), 5)
        self.assertRaisesMessage(ValidationError,
                                 'Le nombre maximal de participant inscit a cette seance est déjà atteint')

    def test_with_invalid_data_seance(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]))
        data = {"seance": "test",
                "participant": 19
                }

        request = self.client.post(reverse(URL_NEW_REGISTRATION, args=[self.seance1.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Register.objects.count(), 4)
        self.assertRaises(ValueError)
