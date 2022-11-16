from django.test import TestCase
from django.urls import reverse
from formation_metier.tests.utils import create_test_formation

URL_LIST_FORMATION = 'formation_metier:list_formation'


class ListFormationViewTest(TestCase):

    def test_without_formation(self):
        url = reverse(URL_LIST_FORMATION)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Il n'y a pas de formation organisée")
        self.assertQuerysetEqual(response.context['formation_list'], [])

    def test_with_one_formation(self):
        formation1 = create_test_formation(name="Formation_name_1", code="AAAAA0001")
        url = reverse(URL_LIST_FORMATION)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, formation1.name)
        self.assertQuerysetEqual(
            response.context['formation_list'],
            [formation1],
        )

    def test_with_two_formation(self):
        formation1 = create_test_formation(name="Formation_name_1", code="AAAAA0001")
        formation2 = create_test_formation(name="Formation_name_2", code="AAAAA0002")
        url = reverse(URL_LIST_FORMATION)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['formation_list'],
            [formation1, formation2],
            ordered=False,
        )
