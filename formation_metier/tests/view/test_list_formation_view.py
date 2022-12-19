from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from formation_metier.tests.factories.formation import FormationFactory
from formation_metier.tests.factories.employe_uclouvain import EmployeUCLouvainWithPermissionsFactory
from formation_metier.models.employe_uclouvain import RoleFormationFareEnum

URL_LIST_FORMATION = 'formation_metier:liste_formation'


class ListFormationViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.date = datetime.today()
        cls.employe_uclouvain = EmployeUCLouvainWithPermissionsFactory('access_to_formation_fare',
                                                                       'view_formation',
                                                                       role=RoleFormationFareEnum.PARTICIPANT)

    def test_should_authorise_access_to_user(self):
        self.client.force_login(user=self.employe_uclouvain.user)
        response = self.client.get(reverse(URL_LIST_FORMATION))
        self.assertEqual(response.status_code, 200)

    def test_should_deny_access_user_case_not_logged(self):
        response = self.client.get(reverse(URL_LIST_FORMATION))
        self.assertEqual(response.status_code, 302)

    def test_should_display_any_formation(self):
        self.client.force_login(user=self.employe_uclouvain.user)
        url = reverse(URL_LIST_FORMATION)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['formation_liste'], [])

    def test_should_display_one_formation(self):
        self.client.force_login(user=self.employe_uclouvain.user)
        formation = FormationFactory()
        url = reverse(URL_LIST_FORMATION)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['formation_liste'],
            [formation],
        )

    def test_should_display_two_formation(self):
        self.client.force_login(user=self.employe_uclouvain.user)
        formation1 = FormationFactory()
        formation2 = FormationFactory()
        url = reverse(URL_LIST_FORMATION)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['formation_liste'],
            [formation1, formation2],
            ordered=False,
        )
