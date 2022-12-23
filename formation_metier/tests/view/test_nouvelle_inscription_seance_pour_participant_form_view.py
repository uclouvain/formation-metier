import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from formation_metier.models.inscription import Inscription
from formation_metier.tests.factories.employe_uclouvain import EmployeUCLouvainFactory
from formation_metier.tests.factories.inscription import InscriptionFactory
from formation_metier.tests.factories.seance import SeanceFactory
from formation_metier.views.inscription_seance_pour_participant_view import InscriptionSeancePourParticipantView

URL = "formation_metier:" + InscriptionSeancePourParticipantView.name


class NouvelleInscriptionSeancePourParticipantFormViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.date = datetime.datetime.today()
        cls.employe_ucl = EmployeUCLouvainFactory()
        cls.seance = SeanceFactory()

    def test_should_authorise_access_to_user(self):
        self.client.force_login(user=self.employe_ucl.user)
        response = self.client.get(reverse(URL, args=[self.seance.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('inscription_seance_pour_participant.html')

    def test_should_deny_access_case_user_not_logged(self):
        response = self.client.get(reverse(URL, args=[self.seance.id]))
        self.assertEqual(response.status_code, 302)

    def test_should_add_inscription(self):
        self.client.force_login(user=self.employe_ucl.user)
        response = self.client.get(reverse(URL, args=[self.seance.id]))
        self.assertEqual(response.status_code, 200)
        request = self.client.post(reverse(URL, args=[self.seance.id]))
        self.assertEqual(request.status_code, 302)
        self.assertEqual(Inscription.objects.count(), 1)

    def test_should_raise_error_case_inscription_close(self):
        seance = SeanceFactory(participant_max_number=2)
        inscription1 = InscriptionFactory(seance=seance)
        inscription2 = InscriptionFactory(seance=seance)
        self.client.force_login(user=self.employe_ucl.user)
        response = self.client.get(reverse(URL, args=[seance.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Inscription.objects.count(), 2)
        request = self.client.post(reverse(URL, args=[seance.id]))
        self.assertEqual(request.status_code, 200)
        self.assertRaisesMessage(
            ValidationError,
            "Le nombre maximal de participant inscit a cette seance est déjà atteint"
        )
        self.assertEqual(Inscription.objects.count(), 2)

    def test_should_raise_error_case_user_deja_inscrit(self):
        Inscription.objects.create(seance=self.seance, participant=self.employe_ucl)
        self.client.force_login(user=self.employe_ucl.user)
        response = self.client.get(reverse(URL, args=[self.seance.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Inscription.objects.count(), 1)
        request = self.client.post(reverse(URL, args=[self.seance.id]))
        self.assertEqual(request.status_code, 200)
        self.assertRaises(ValidationError)
        self.assertEqual(Inscription.objects.count(), 1)
