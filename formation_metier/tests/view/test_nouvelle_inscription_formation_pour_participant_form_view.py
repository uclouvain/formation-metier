import datetime

from django.test import TestCase
from django.urls import reverse

from formation_metier.tests.factories.employe_uclouvain import EmployeUCLouvainFactory
from formation_metier.tests.factories.formation import FormationFactory
from formation_metier.views import InscriptionAUneFormation

URL = "formation_metier:" + InscriptionAUneFormation.name


class NouvelleInscriptionFormationPourParticipantFormViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.date = datetime.today()
        cls.employe_ucl = EmployeUCLouvainFactory()
        cls.formation = FormationFactory()

    def test_should_authorise_access_to_user(self):
        self.client.force_login(user=self.employe_ucl.user)
        response = self.client.get(reverse(URL, args=[self.formation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('inscription_formation_pour_participant.html')

    def test_should_deny_access_case_user_not_logged(self):
        pass

    def test_should_just_add_one_inscription(self):
        pass

    def test_should_add_and_delete_inscription(self):
        pass

    def test_should_delete_inscription(self):
        pass

    def test_should_raise_error(self):
        pass
