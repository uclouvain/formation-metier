from datetime import datetime
from pprint import pprint

from django.contrib.auth.models import Group, Permission, User
from django.test import TestCase
from django.urls import reverse

from formation_metier.enums.roles_osis_enum import ROLES_OSIS_CHOICES
from formation_metier.models.person import RoleFormationFareEnum
from formation_metier.tests.utils import create_test_formation, create_test_seance, create_test_user, \
    create_test_formateur, create_test_person

URL_DETAIL_FORMATION_VIEW = 'formation_metier:detail_formation'


class DetailFormationViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.date = datetime.today()
        cls.user1 = create_test_user(username="user1", password="password123")
        cls.user1.user_permissions.add(Permission.objects.get(codename='access_to_formation_fare'))
        cls.user1.user_permissions.add(Permission.objects.get(codename='view_formation'))
        cls.user1 = User.objects.get(pk=cls.user1.pk)
        cls.person1 = create_test_person(name="formateur1",
                                         number_fgs="AAAA0001",
                                         role_formation_metier=RoleFormationFareEnum.FORMATEUR,
                                         user=cls.user1
                                         )
        cls.formateur1 = create_test_formateur(person=cls.person1)

        cls.formation1 = create_test_formation(name="Formation_name_1", code="AAAA01",
                                               public_cible=ROLES_OSIS_CHOICES[1])
        cls.formation2 = create_test_formation(name="Formation_name_2", code="AAAA02",
                                               public_cible=ROLES_OSIS_CHOICES[1])
        cls.formation3 = create_test_formation(name="Formation_name_3", code="AAAA03",
                                               public_cible=ROLES_OSIS_CHOICES[1])
        cls.seance1 = create_test_seance(formation=cls.formation2,
                                          seance_date=cls.date,
                                          participant_max_number=10,
                                          local="L001",
                                          formateur=cls.formateur1,
                                          duree=60
                                          )
        cls.seance2 = create_test_seance(formation=cls.formation1,
                                          seance_date=cls.date,
                                          participant_max_number=10,
                                          local="L002",
                                          formateur=cls.formateur1,
                                          duree=60
                                          )
        cls.seance3 = create_test_seance(formation=cls.formation1,
                                          seance_date=cls.date,
                                          participant_max_number=10,
                                          local="L003",
                                          formateur=cls.formateur1,
                                          duree=60
                                          )

    def test_without_seance(self):
        self.client.force_login(user=self.user1)
        url = reverse(URL_DETAIL_FORMATION_VIEW, args=[self.formation3.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.formation3.name)
        self.assertContains(response, self.formation3.code)
        self.assertContains(response, self.formation3.description)
        self.assertContains(response,
                            "Il n'y a pas de seance actuellement organisé pour la formation : " + self.formation3.name)

    def test_with_one_seance_for_formation(self):
        self.client.force_login(user=self.user1)
        url = reverse(URL_DETAIL_FORMATION_VIEW, args=[self.formation2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.formation2.name)
        self.assertContains(response, self.formation2.code)
        self.assertContains(response, self.formation2.description)
        self.assertContains(response, self.seance1.participant_max_number)
        self.assertContains(response, self.seance1.local)
        self.assertContains(response, self.seance1.formateur)
        self.assertEqual(response.context["formation"], self.formation2)
        self.assertNotEqual(response.context["formation"], self.formation1)
        self.assertNotEqual(response.context["formation"], self.formation3)

    def test_with_many_seance_not_all_for_formation(self):
        self.client.force_login(user=self.user1)
        url = reverse(URL_DETAIL_FORMATION_VIEW, args=[self.formation1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.formation1.name)
        self.assertContains(response, self.formation1.code)
        self.assertNotContains(response, self.formation2.name)
        self.assertNotContains(response, self.formation2.code)
        self.assertNotContains(response, self.seance1.local)
        self.assertContains(response, self.seance3.local)
        self.assertContains(response, self.seance2.local)
        self.assertContains(response, self.seance3.participant_max_number)
        self.assertContains(response, self.seance2.participant_max_number)
        self.assertContains(response, self.seance2.formateur)
        self.assertContains(response, self.seance3.formateur)
        self.assertEqual(response.context["formation"], self.formation1)
        self.assertNotEqual(response.context["formation"], self.formation2)
