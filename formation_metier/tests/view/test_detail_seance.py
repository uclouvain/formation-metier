from django.test import TestCase

from django.urls import reverse
from django.utils import timezone

from formation_metier.models.employe_uclouvain import RoleFormationFareEnum
from formation_metier.tests.factories.employe_uclouvain import EmployeUCLouvainWithPermissionsFactory
from formation_metier.tests.factories.seance import SeanceFactory
from formation_metier.tests.factories.inscription import InscriptionFactory

URL_DETAIL_SEANCE_VIEW = 'formation_metier:detail_seance'


class DetailSeanceViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.date = timezone.now()
        cls.employe_uclouvain = EmployeUCLouvainWithPermissionsFactory('access_to_formation_fare',
                                                                       'view_inscription',
                                                                       'add_inscription',
                                                                       'view_seance',
                                                                       role=RoleFormationFareEnum.PARTICIPANT)
        cls.seance = SeanceFactory()

    def test_should_authorise_access_to_user(self):
        self.client.force_login(user=self.employe_uclouvain.user)
        url = reverse(URL_DETAIL_SEANCE_VIEW, args=[self.seance.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_should_deny_access_user_case_not_logged(self):
        url = reverse(URL_DETAIL_SEANCE_VIEW, args=[self.seance.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_should_deny_access_user_case_not_have_perm_access_to_formation_fare(self):
        employe_uclouvain = EmployeUCLouvainWithPermissionsFactory('view_seance',
                                                                   'add_inscription',
                                                                   'view_inscription',
                                                                   role=RoleFormationFareEnum.PARTICIPANT)
        self.client.force_login(user=employe_uclouvain.user)
        url = reverse(URL_DETAIL_SEANCE_VIEW, args=[self.seance.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_should_deny_access_user_case_not_have_perm_view_seance(self):
        employe_uclouvain = EmployeUCLouvainWithPermissionsFactory('access_to_formation_fare',
                                                                   'add_inscription',
                                                                   'view_inscription',
                                                                   role=RoleFormationFareEnum.PARTICIPANT)
        self.client.force_login(user=employe_uclouvain.user)
        url = reverse(URL_DETAIL_SEANCE_VIEW, args=[self.seance.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_should_deny_access_user_case_not_have_perm_view_register(self):
        employe_uclouvain = EmployeUCLouvainWithPermissionsFactory('access_to_formation_fare',
                                                                   'view_seance',
                                                                   'add_inscription',
                                                                   role=RoleFormationFareEnum.PARTICIPANT)
        self.client.force_login(user=employe_uclouvain.user)
        url = reverse(URL_DETAIL_SEANCE_VIEW, args=[self.seance.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_should_display_any_register(self):
        self.client.force_login(user=self.employe_uclouvain.user)
        url = reverse(URL_DETAIL_SEANCE_VIEW, args=[self.seance.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.seance.formation)
        self.assertContains(response, self.seance.formateur)
        self.assertContains(response, self.seance.participant_max_number)
        self.assertEqual(response.context["seance"].register_set.count(), 0)
        self.assertContains(response, "Il n'y a aucun participant d'inscrit pour l'instant")

    def test_should_not_display_all_register(self):
        self.client.force_login(user=self.employe_uclouvain.user)
        register1 = InscriptionFactory()
        register2 = InscriptionFactory(seance=register1.seance)
        register3 = InscriptionFactory()
        register4 = InscriptionFactory()
        url = reverse(URL_DETAIL_SEANCE_VIEW, args=[register1.seance.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, register1.seance.formation)
        self.assertContains(response, register1.seance.formateur)
        self.assertContains(response, register1.seance.participant_max_number)
        self.assertContains(response, register1.participant.name)
        self.assertContains(response, register1.participant.number_fgs)
        self.assertContains(response, register2.participant.name)
        self.assertContains(response, register2.participant.number_fgs)
        self.assertNotContains(response, register3.participant.name)
        self.assertNotContains(response, register3.participant.number_fgs)
        self.assertNotContains(response, register4.participant.name)
        self.assertNotContains(response, register4.participant.number_fgs)
        self.assertEqual(response.context["seance"], register1.seance)
        self.assertEqual(response.context["seance"], register2.seance)
        self.assertNotEqual(response.context["seance"], register3.seance)
        self.assertNotEqual(response.context["seance"], register4.seance)
        self.assertEqual(response.context["seance"].register_set.count(), 2)
