from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from formation_metier.models.inscription import Inscription
from formation_metier.tests.factories.employe_uclouvain import EmployeUCLouvainFactory
from formation_metier.tests.factories.formation import FormationFactory
from formation_metier.tests.factories.inscription import InscriptionFactory
from formation_metier.tests.factories.seance import SeanceFactory
from formation_metier.views import InscriptionFormationPourParticipant

URL = "formation_metier:" + InscriptionFormationPourParticipant.name


class NouvelleInscriptionFormationPourParticipantFormViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.date = datetime.today()
        cls.employe_ucl = EmployeUCLouvainFactory()
        cls.formation = FormationFactory()
        cls.seance1 = SeanceFactory(formation=cls.formation)
        cls.seance2 = SeanceFactory(formation=cls.formation)
        cls.seance3 = SeanceFactory(formation=cls.formation)
        cls.inscription1 = InscriptionFactory(seance=cls.seance1, participant=cls.employe_ucl)
        cls.inscription2 = InscriptionFactory(seance=cls.seance2, participant=cls.employe_ucl)

    def test_should_authorise_access_to_user(self):
        self.client.force_login(user=self.employe_ucl.user)
        response = self.client.get(reverse(URL, args=[self.formation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('inscription_formation_pour_participant.html')

    def test_should_deny_access_case_user_not_logged(self):
        response = self.client.get(reverse(URL, args=[self.formation.id]))
        self.assertEqual(response.status_code, 302)

    def test_should_add_one_inscription(self):
        self.assertEqual(Inscription.objects.count(), 2)
        self.client.force_login(user=self.employe_ucl.user)
        response = self.client.get(reverse(URL, args=[self.formation.id]))
        self.assertEqual(response.status_code, 200)
        request = self.client.post(
            reverse(URL, args=[self.formation.id]),
            data={
                'seance': [
                    str(self.seance1.id),
                    str(self.seance2.id),
                    str(self.seance3.id),
                ]
            }
        )
        self.assertEqual(request.status_code, 302)
        self.assertEqual(Inscription.objects.count(), 3)

    def test_should_delete_one_inscription(self):
        self.assertEqual(Inscription.objects.count(), 2)
        self.client.force_login(user=self.employe_ucl.user)
        response = self.client.get(reverse(URL, args=[self.formation.id]))
        self.assertEqual(response.status_code, 200)
        request = self.client.post(
            reverse(URL, args=[self.formation.id]),
            data={
                'seance': [
                    str(self.seance1.id),
                ]
            }
        )
        self.assertEqual(request.status_code, 302)
        self.assertEqual(Inscription.objects.count(), 1)

    def test_should_add_and_delete_inscription(self):
        self.assertEqual(Inscription.objects.count(), 2)
        self.client.force_login(user=self.employe_ucl.user)
        response = self.client.get(reverse(URL, args=[self.formation.id]))
        self.assertEqual(response.status_code, 200)
        request = self.client.post(
            reverse(URL, args=[self.formation.id]),
            data={
                'seance': [
                    str(self.seance1.id),
                    str(self.seance3.id),
                ]
            }
        )
        self.assertEqual(request.status_code, 302)
        self.assertEqual(Inscription.objects.count(), 2)
