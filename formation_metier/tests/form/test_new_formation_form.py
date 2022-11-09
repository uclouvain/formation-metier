from datetime import datetime

from django.test import TestCase

from django.urls import reverse

from formation_metier.forms.new_formation_form import NewFormationForm
from formation_metier.models.formation import Formation
from formation_metier.tests.utils import create_test_formation

URL_NEW_FORMATION_VIEW = reverse('formation_metier:new_formation')


class NewFormationFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.formation1 = create_test_formation(name="formation_test_1", code="AAAAA0001")

    def test_get(self):
        response = self.client.get(URL_NEW_FORMATION_VIEW)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h2>Nouvelle formation</h2>", html=True)

    def test_with_valid_data_and_respected_constaint(self):
        data = {"name": "formation_test_2",
                "code": "AAAAA0002",
                "description": "formation de test"}
        response = self.client.post(URL_NEW_FORMATION_VIEW, data=data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/index")

    def test_with_valid_data_and_unrespected_constaint(self):
        data = {"name": "formation_test_2",
                "code": "AAAAA0001",
                "description": "formation de test"}
        response = self.client.get(URL_NEW_FORMATION_VIEW)
        request = self.client.post(URL_NEW_FORMATION_VIEW, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 200)
        self.assertFormError(request, 'form', "code", ["Un objet Formation avec ce champ Code existe déjà."])

    # a faire si CharFiled ne convertis pas automatiquement en str
    def test_with_invalid_data_name(self):
        data = {"name": True,
                "code": "AAAAA0002",
                "description": "formation de test"}
        response = self.client.get(URL_NEW_FORMATION_VIEW)
        request = self.client.post(URL_NEW_FORMATION_VIEW, data=data)

        self.assertEqual(response.status_code, 200)
        # self.assertEqual(request.status_code, 200)
        # self.assertEqual(Formation.objects.count(), 1)
        # self.assertFormError(request, 'form', "name", ["Un objet Formation avec ce champ Code existe déjà."])

    def test_with_invalid_data_code(self):
        data = {"name": "Fromation_test_2",
                "code": "AAAAA0002A",
                "description": "formation de test"}
        response = self.client.get(URL_NEW_FORMATION_VIEW)
        request = self.client.post(URL_NEW_FORMATION_VIEW, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Formation.objects.count(), 1)
        self.assertFormError(request, 'form', "code",
                             [f'Assurez-vous que cette valeur comporte au plus 9 caractères (actuellement {len(data["code"])}).'])

    # a faire si CharFiled ne convertis pas automatiquement en str
    def test_with_invalid_data_description(self):
        response = self.client.get(URL_NEW_FORMATION_VIEW)

