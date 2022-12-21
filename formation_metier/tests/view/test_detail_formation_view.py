from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from formation_metier.models.employe_uclouvain import RoleFormationFareEnum
from formation_metier.tests.factories.employe_uclouvain import EmployeUCLouvainWithPermissionsFactory
from formation_metier.tests.factories.seance import SeanceFactory
from formation_metier.tests.factories.formation import FormationFactory

URL_DETAIL_FORMATION_VIEW = 'formation_metier:detail_formation'


class DetailFormationViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.date = datetime.today()
        cls.employe_uclouvain = EmployeUCLouvainWithPermissionsFactory('access_to_formation_fare',
                                                                       'view_formation',
                                                                       'view_seance',
                                                                       role=RoleFormationFareEnum.PARTICIPANT)
        cls.formation = FormationFactory()

    def test_should_authorise_access_to_user(self):
        self.client.force_login(user=self.employe_uclouvain.user)
        url = reverse(URL_DETAIL_FORMATION_VIEW, args=[self.formation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_should_deny_access_user_case_not_logged(self):
        url = reverse(URL_DETAIL_FORMATION_VIEW, args=[self.formation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_should_deny_access_user_case_not_have_perm_access_to_formation_fare(self):
        employe_uclouvain = EmployeUCLouvainWithPermissionsFactory('view_formation',
                                                                   'view_formation',
                                                                   role=RoleFormationFareEnum.PARTICIPANT)
        self.client.force_login(user=employe_uclouvain.user)
        url = reverse(URL_DETAIL_FORMATION_VIEW, args=[self.formation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_should_deny_access_user_case_not_have_perm_view_seance(self):
        employe_uclouvain = EmployeUCLouvainWithPermissionsFactory('access_to_formation_fare',
                                                                   'view_formation',
                                                                   role=RoleFormationFareEnum.PARTICIPANT)
        self.client.force_login(user=employe_uclouvain.user)
        url = reverse(URL_DETAIL_FORMATION_VIEW, args=[self.formation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_should_deny_access_user_case_not_have_perm_view_formation(self):
        employe_uclouvain = EmployeUCLouvainWithPermissionsFactory('access_to_formation_fare',
                                                                   'view_seance',
                                                                   role=RoleFormationFareEnum.PARTICIPANT)
        self.client.force_login(user=employe_uclouvain.user)
        url = reverse(URL_DETAIL_FORMATION_VIEW, args=[self.formation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_should_display_any_seance(self):
        self.client.force_login(user=self.employe_uclouvain.user)
        url = reverse(URL_DETAIL_FORMATION_VIEW, args=[self.formation.id])
        seance = SeanceFactory()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            "Il n'y a pas de seance actuellement organisé pour la formation : " + self.formation.name)

    def test_with_one_seance_for_formation(self):
        self.client.force_login(user=self.employe_uclouvain.user)
        seance = SeanceFactory()
        url = reverse(URL_DETAIL_FORMATION_VIEW, args=[seance.formation_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["formation"], seance.formation)
        self.assertNotEqual(response.context["formation"], self.formation)

    def test_with_many_seance_not_all_for_formation(self):
        self.client.force_login(user=self.employe_uclouvain.user)
        seance1 = SeanceFactory(formation=self.formation)
        seance2 = SeanceFactory(formation=seance1.formation)
        seance3 = SeanceFactory()
        seance4 = SeanceFactory()
        url = reverse(URL_DETAIL_FORMATION_VIEW, args=[self.formation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["formation"], seance1.formation)
        self.assertEqual(response.context["formation"], seance2.formation)
        self.assertNotEqual(response.context["formation"], seance3.formation)
        self.assertNotEqual(response.context["formation"], seance4.formation)
