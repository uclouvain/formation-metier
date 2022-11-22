from datetime import datetime
from pprint import pprint

from django.core.exceptions import ValidationError
from django.test import TestCase

from django.urls import reverse
from formation_metier.models.person import Person
from formation_metier.models.session import Session
from formation_metier.tests.utils import create_test_formation, create_test_session, create_test_person, \
    create_test_formateur
from formation_metier.enums.roles_osis_enum import ROLES_OSIS_CHOICES

URL_NEW_SESSION_VIEW = 'formation_metier:new_session'


class NewSessionFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.date = datetime.today()
        cls.formation1 = create_test_formation(name="formation_test_1", code="AAAAA0001")
        cls.person1 = create_test_person(name="test", number_fgs="AAA01",
                                         role_formation_metier=Person.ROLES_FORMATION_FARE[1])
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
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h2>Nouvelle session</h2>", html=True)
        self.assertTemplateUsed('new_session.html')

    def test_with_valid_data_and_respected_constaint(self):
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
        print(self.date)
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
