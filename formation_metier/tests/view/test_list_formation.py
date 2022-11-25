from datetime import datetime

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse
from formation_metier.tests.utils import create_test_formation, create_test_user

URL_LIST_FORMATION = 'formation_metier:list_formation'


class ListFormationViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.date = datetime.today()
        cls.user1 = create_test_user(username="user1", password="password123")
        cls.user1.user_permissions.add(Permission.objects.get(codename='access_to_formation_fare'))
        cls.user1.user_permissions.add(Permission.objects.get(codename='view_formation'))
        cls.user1 = User.objects.get(pk=cls.user1.pk)

    def test_without_formation(self):
        self.client.force_login(user=self.user1)
        url = reverse(URL_LIST_FORMATION)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Il n'y a pas de formation organisée")
        self.assertQuerysetEqual(response.context['formation_list'], [])

    def test_with_one_formation(self):
        self.client.force_login(user=self.user1)
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
        self.client.force_login(user=self.user1)
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
