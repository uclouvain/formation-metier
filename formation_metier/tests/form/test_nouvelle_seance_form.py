from datetime import datetime
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from formation_metier.models.seance import Seance
from formation_metier.tests.factories.employe_uclouvain import EmployeUCLouvainWithPermissionsFactory
from formation_metier.tests.factories.seance import SeanceFactory
URL_NEW_SESSION_VIEW = 'formation_metier:nouvelle_seance'


class NouvelleSeanceFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.date = datetime.today()
        cls.employe_ucl = EmployeUCLouvainWithPermissionsFactory('access_to_formation_fare', 'add_seance')
        cls.seance = SeanceFactory()

    def test_should_authorise_access_to_formateur(self):
        self.client.force_login(user=self.employe_ucl.user)
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.seance.formation.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h2>Nouvelle séance</h2>", html=True)
        self.assertTemplateUsed('new_session.html')

    def test_should_deny_access_case_user_not_logged(self):
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.seance.formation.id]))
        self.assertEqual(response.status_code, 302)

    def test_should_deny_access_case_user_not_have_permission_access_to_formation_fare(self):
        employe_ucl = EmployeUCLouvainWithPermissionsFactory('add_seance')
        self.client.force_login(user=employe_ucl.user)
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.seance.formation.id]))
        self.assertEqual(response.status_code, 403)

    def test_should_deny_access_case_user_not_have_permission_add_seance(self):
        employe_ucl = EmployeUCLouvainWithPermissionsFactory('access_to_formation_fare')
        self.client.force_login(user=employe_ucl.user)
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.seance.formation.id]))
        self.assertEqual(response.status_code, 403)

    def test_should_not_raise_exception(self):
        self.client.force_login(user=self.employe_ucl.user)
        data = {"formation": self.seance.formation,
                "seance_date": self.date,
                "participant_max_number": 10,
                "local": "L002",
                "formateur": self.employe_ucl,
                "duree": 20
                }
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.seance.formation.id]))
        self.assertEqual(response.status_code, 200)
        request = self.client.post(reverse(URL_NEW_SESSION_VIEW, args=[self.seance.formation.id]), data=data)
        Seance.objects.create(formation=self.seance.formation,
                              seance_date=self.date,
                              participant_max_number=10,
                              local="L002",
                              formateur=self.employe_ucl,
                              duree=20)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Seance.objects.count(), 2)

    def test_should_raise_validation_error_case_code_date_formateur_already_exist(self):
        self.client.force_login(user=self.employe_ucl.user)
        data = {"formation": "test",
                "seance_date": self.date,
                "participant_max_number": 10,
                "local": "L001",
                "formateur": self.employe_ucl,
                'duree': 60}
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.seance.formation.id]))
        request = self.client.post(reverse(URL_NEW_SESSION_VIEW, args=[self.seance.formation.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Seance.objects.count(), 1)
        self.assertRaisesMessage(ValidationError,
                                 'Un objet Seance avec ces champs Seance date, Local et Formateur existe déjà.')

    def test_should_raise_validation_error_case_duree_value(self):
        self.client.force_login(user=self.employe_ucl.user)
        data = {"formation": "test",
                "seance_date": self.date,
                "participant_max_number": 10,
                "local": "L001",
                "formateur": self.employe_ucl,
                'duree': 700}
        response = self.client.get(reverse(URL_NEW_SESSION_VIEW, args=[self.seance.formation.id]))
        request = self.client.post(reverse(URL_NEW_SESSION_VIEW, args=[self.seance.formation.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Seance.objects.count(), 1)
        self.assertRaisesMessage(ValidationError,
                                 'Assurez-vous que cette valeur est inférieure ou égale à 600.')
