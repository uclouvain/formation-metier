from datetime import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from formation_metier.forms.new_formation_form import NewFormationForm
from formation_metier.models.formation import Formation
from formation_metier.models.session import Session
from formation_metier.tests.utils import create_test_formation, create_test_session

URL_NEW_SESSION_VIEW = 'formation_metier:new_session'


class NewSessionFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.date = timezone.now()
        cls.formation1 = create_test_formation(name="formation_test_1", code="AAAAA0001")
        cls.session1 = create_test_session(formation=cls.formation1,
                                           session_date=cls.date,
                                           participant_max_number=10,
                                           local="L001",
                                           formateur_id="formateur1",
                                           public_cible=Session.PARTICIPANT
                                           )

    def test_get(self):
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h2>Nouvelle session</h2>", html=True)

    def test_with_valid_data_and_respected_constaint(self):
        data = {"formation": self.formation1,
                "session_date": self.date,
                "participant_max_number": 10,
                "local": "L001",
                "formateur_id": "formateur1",
                "public_cible": Session.PARTICIPANT}
        response = self.client.post(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]), data=data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('formation_metier:detail_formation', args=[self.formation1.id]))

    def test_with_invalid_data_formation(self):
        data = {"formation": "test",
                "session_date": self.date,
                "participant_max_number": 10,
                "local": "L001",
                "formateur_id": "formateur1",
                "public_cible": Session.PARTICIPANT}
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]))
        request = self.client.post(reverse(URL_NEW_SESSION_VIEW, args=[self.formation1.id]), data=data)

        self.assertEqual(response.status_code, 200)
        # self.assertEqual(request.status_code, 200)
        self.assertFormError(request, 'form', "test", ["Un objet Formation avec ce champ Code existe déjà."])

    def test_with_invalid_data_(self):
        data = {"name": True,
                "code": "AAAAA0002",
                "description": "formation de test"}
        response = self.client.get(URL_NEW_FORMATION_VIEW)
        request = self.client.post(URL_NEW_FORMATION_VIEW, data=data)

        self.assertEqual(response.status_code, 200)
        # self.assertEqual(request.status_code, 200)
        # self.assertEqual(Formation.objects.count(), 1)
        # self.assertFormError(request, 'form', "name", ["Un objet Formation avec ce champ Code existe déjà."])
