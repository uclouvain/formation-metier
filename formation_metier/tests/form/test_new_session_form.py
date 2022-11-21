from datetime import datetime
from pprint import pprint

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from formation_metier.forms.new_formation_form import NewFormationForm
from formation_metier.models.formation import Formation
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
        print(cls.date)
        cls.formation1 = create_test_formation(name="formation_test_1", code="AAAAA0001")
        cls.person1 = create_test_person(name="test", number_fgs="AAA01",
                                         role_formation_metier=Person.ROLES_FORMATION_FARE[1])
        cls.formateur1 = create_test_formateur(person=cls.person1)
        cls.session1 = create_test_session(formation=cls.formation1,
                                           session_date=cls.date,
                                           participant_max_number=10,
                                           local="L001",
                                           formateur=cls.formateur1,
                                           public_cible=ROLES_OSIS_CHOICES[1]
                                           )

    def test_get(self):
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h2>Nouvelle session</h2>", html=True)

    def test_with_valid_data_and_respected_constaint(self):
        data = {"formation": self.formation1,
                "session_date": self.date,
                "participant_max_number": 10,
                "local": "L002",
                "formateur": self.formateur1,
                "public_cible": ROLES_OSIS_CHOICES[1]}
        response = self.client.post(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]), data=data)
        print(response)
        print(reverse('formation_metier:detail_formation', args=[self.formation1.id]))
        Session.objects.create(formation=self.formation1,
                               session_date=self.date,
                               participant_max_number=10,
                               local="L002",
                               formateur=self.formateur1,
                               public_cible=ROLES_OSIS_CHOICES[1])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Session.objects.count(), 2)

    def test_with_invalid_data_formation(self):
        print(self.date)
        data = {"formation": "test",
                "session_date": self.date,
                "participant_max_number": 10,
                "local": "L001",
                "formateur": self.formateur1,
                "public_cible": ROLES_OSIS_CHOICES[1]}
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]))
        request = self.client.post(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Session.objects.count(), 1)
