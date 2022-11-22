from django.test import TestCase

from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import localtime

from formation_metier.enums.roles_osis_enum import ROLES_OSIS_CHOICES
from formation_metier.models.session import Session
from formation_metier.tests.utils import create_test_formation, create_test_session

URL_DETAIL_FORMATION_VIEW = 'formation_metier:detail_formation'


class DetailFormationViewTest(TestCase):
    date = timezone.now()

    def test_without_session(self):
        formation1 = create_test_formation(name="Formation_name_1", code="AAAAA0001")
        url = reverse(URL_DETAIL_FORMATION_VIEW, args=[formation1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, formation1.name)
        self.assertContains(response, formation1.code)
        self.assertContains(response, formation1.description)
        self.assertContains(response,
                            "Il n'y a pas de session actuellement organisé pour la formation : " + formation1.name)

    def test_with_one_session_for_formation(self):
        formation1 = create_test_formation(name="Formation_name_1", code="AAAAA0001")
        session1 = create_test_session(formation=formation1,
                                       session_date=self.date,
                                       participant_max_number=10,
                                       local="L001",
                                       formateur="formateur1",
                                       public_cible=ROLES_OSIS_CHOICES.PARTICIPANT
                                       )
        url = reverse(URL_DETAIL_FORMATION_VIEW, args=[formation1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, formation1.name)
        self.assertContains(response, formation1.code)
        self.assertContains(response, formation1.description)
        self.assertContains(response, session1.participant_max_number)
        self.assertContains(response, session1.local)
        self.assertContains(response, session1.formateur)
        self.assertEqual(response.context["formation"], formation1)

    def test_with_one_session_not_for_formation(self):
        formation1 = create_test_formation(name="Formation_name_1", code="AAAAA0001")
        formation2 = create_test_formation(name="Formation_name_2", code="AAAAA0002")
        session1 = create_test_session(formation=formation2,
                                       session_date=self.date,
                                       participant_max_number=10,
                                       local="L001",
                                       formateur="formateur1",
                                       public_cible=ROLES_OSIS_CHOICES.PARTICIPANT
                                       )
        url = reverse(URL_DETAIL_FORMATION_VIEW, args=[formation1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, formation1.name)
        self.assertContains(response, formation1.code)
        self.assertNotContains(response, formation2.name)
        self.assertNotContains(response, formation2.code)
        self.assertNotContains(response, session1.local)
        self.assertNotContains(response, session1.formateur)
        self.assertEqual(response.context["formation"], formation1)
        self.assertNotEqual(response.context["formation"], formation2)

    def test_with_many_session_not_all_for_formation(self):
        formation1 = create_test_formation(name="Formation_name_1", code="AAAAA0001")
        formation2 = create_test_formation(name="Formation_name_2", code="AAAAA0002")
        session1 = create_test_session(formation=formation2,
                                       session_date=self.date,
                                       participant_max_number=10,
                                       local="L001",
                                       formateur="formateur1",
                                       public_cible=ROLES_OSIS_CHOICES.PARTICIPANT
                                       )
        session2 = create_test_session(formation=formation1,
                                       session_date=self.date,
                                       participant_max_number=10,
                                       local="L002",
                                       formateur="formateur2",
                                       public_cible=ROLES_OSIS_CHOICES.PARTICIPANT
                                       )
        session3 = create_test_session(formation=formation1,
                                       session_date=self.date,
                                       participant_max_number=10,
                                       local="L003",
                                       formateur="formateur3",
                                       public_cible=ROLES_OSIS_CHOICES.PARTICIPANT
                                       )
        url = reverse(URL_DETAIL_FORMATION_VIEW, args=[formation1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, formation1.name)
        self.assertContains(response, formation1.code)
        self.assertNotContains(response, formation2.name)
        self.assertNotContains(response, formation2.code)
        self.assertNotContains(response, session1.local)
        self.assertContains(response, session3.local)
        self.assertContains(response, session2.local)
        self.assertContains(response, session3.participant_max_number)
        self.assertContains(response, session2.participant_max_number)
        self.assertContains(response, session2.formateur)
        self.assertContains(response, session3.formateur)
        self.assertEqual(response.context["formation"], formation1)
        self.assertNotEqual(response.context["formation"], formation2)
