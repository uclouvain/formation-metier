from django.test import TestCase
from datetime import datetime

from django.urls import reverse
from django.core.exceptions import ValidationError

from formation_metier.enums.roles_osis_enum import ROLES_OSIS_CHOICES
from formation_metier.models.person import Person, RoleFormationFareEnum
from formation_metier.models.register import Register
from formation_metier.tests.utils import create_test_formation, create_test_session, create_test_formateur, \
    create_test_person, create_test_register, create_test_participant, create_test_user

URL_NEW_REGISTRATION = 'formation_metier:detail_session'


class NewRegisterFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.date = datetime.today()
        cls.user1 = create_test_user(username="user1", password="password123")
        cls.formation1 = create_test_formation(name="formation_test_1", code="AAAAA0001")

        cls.person1 = create_test_person(name="Formateur1",
                                         number_fgs="AAA01",
                                         role_formation_metier=RoleFormationFareEnum.PARTICIPANT)
        cls.person2 = create_test_person(name="Participant1",
                                         number_fgs="AAA02",
                                         role_formation_metier=RoleFormationFareEnum.PARTICIPANT)
        cls.person3 = create_test_person(name="Participant2",
                                         number_fgs="AAA03",
                                         role_formation_metier=RoleFormationFareEnum.PARTICIPANT)
        cls.person4 = create_test_person(name="Participant3",
                                         number_fgs="AAA04",
                                         role_formation_metier=RoleFormationFareEnum.PARTICIPANT)
        cls.person5 = create_test_person(name="Participant4",
                                         number_fgs="AAA05",
                                         role_formation_metier=RoleFormationFareEnum.PARTICIPANT)
        cls.person6 = create_test_person(name="Participant5",
                                         number_fgs="AAA06",
                                         role_formation_metier=RoleFormationFareEnum.PARTICIPANT)
        cls.person7 = create_test_person(name="Participant6",
                                         number_fgs="AAA07",
                                         role_formation_metier=RoleFormationFareEnum.PARTICIPANT)

        cls.formateur1 = create_test_formateur(person=cls.person1)

        cls.session1 = create_test_session(formation=cls.formation1,
                                           session_date=cls.date,
                                           participant_max_number=5,
                                           local="L001",
                                           formateur=cls.formateur1,
                                           public_cible=ROLES_OSIS_CHOICES[1],
                                           duree=60
                                           )

        cls.participant1 = create_test_participant(person=cls.person2)
        cls.participant2 = create_test_participant(person=cls.person3)
        cls.participant3 = create_test_participant(person=cls.person4)
        cls.participant4 = create_test_participant(person=cls.person5)
        cls.participant5 = create_test_participant(person=cls.person6)
        cls.participant6 = create_test_participant(person=cls.person7)

        cls.register1 = create_test_register(session=cls.session1, participant=cls.participant1)
        cls.register2 = create_test_register(session=cls.session1, participant=cls.participant2)
        cls.register3 = create_test_register(session=cls.session1, participant=cls.participant3)
        cls.register4 = create_test_register(session=cls.session1, participant=cls.participant4)

    def test_get(self):
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.session1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"<h2>Formation : {self.formation1.name}</h2>", html=True)
        self.assertTemplateUsed('detail_session.html')

    def test_with_valid_data_and_respected_constaint(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.session1.id]))
        data = {"session": self.session1,
                "participant": self.participant5.id
                }

        request = self.client.post(reverse(URL_NEW_REGISTRATION, args=[self.session1.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 302)
        self.assertEqual(Register.objects.count(), 5)

    def test_with_valid_data_and_unrespected_constaint(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.session1.id]))
        data = {"session": self.session1,
                "participant": self.participant4.id
                }

        request = self.client.post(reverse(URL_NEW_REGISTRATION, args=[self.session1.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Register.objects.count(), 4)
        self.assertRaisesMessage(ValidationError,
                                 'Un objet Register avec ces champs Session et Participant existe déjà.')

    def test_with_invalid_data_session(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.session1.id]))
        data = {"session": "test",
                "participant": 19
                }

        request = self.client.post(reverse(URL_NEW_REGISTRATION, args=[self.session1.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Register.objects.count(), 4)
        self.assertRaises(ValueError)

