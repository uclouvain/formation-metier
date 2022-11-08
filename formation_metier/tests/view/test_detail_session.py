from django.test import TestCase

from django.urls import reverse
from django.utils import timezone

from formation_metier.models.session import Session
from formation_metier.tests.utils import create_test_formation, create_test_session, create_test_register, \
    create_test_person

URL_DETAIL_FORMATION_VIEW = 'formation_metier:detail_session'


class DetailSessionViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.date = timezone.now()
        cls.person1 = create_test_person(name="person1", number_fgs="XXXXX001", role="formateur")
        cls.person2 = create_test_person(name="person2", number_fgs="XXXXX002", role="participant")
        cls.person3 = create_test_person(name="person3", number_fgs="XXXXX003", role="admin")
        cls.formation1 = create_test_formation(name="Formation_name_1", code="AAAAA0001")
        cls.session1 = create_test_session(formation=cls.formation1,
                                           session_date=cls.date,
                                           participant_max_number=10,
                                           local="L001",
                                           formateur_id="formateur1",
                                           public_cible=Session.PARTICIPANT
                                           )
        cls.session2 = create_test_session(formation=cls.formation1,
                                           session_date=cls.date,
                                           participant_max_number=10,
                                           local="L002",
                                           formateur_id="formateur2",
                                           public_cible=Session.PARTICIPANT
                                           )
        cls.session3 = create_test_session(formation=cls.formation1,
                                           session_date=cls.date,
                                           participant_max_number=10,
                                           local="L002",
                                           formateur_id="formateur2",
                                           public_cible=Session.PARTICIPANT
                                           )
        cls.register1 = create_test_register(session=cls.session2,
                                             participant=cls.person1,
                                             register_date=cls.date)
        cls.register2 = create_test_register(session=cls.session2,
                                             participant=cls.person2,
                                             register_date=cls.date)
        cls.register3 = create_test_register(session=cls.session3,
                                             participant=cls.person3,
                                             register_date=cls.date)

    def test_without_register(self):
        url = reverse(URL_DETAIL_FORMATION_VIEW, args=[self.session1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.session1.formation)
        self.assertContains(response, self.session1.formateur_id)
        self.assertContains(response, self.session1.participant_max_number)
        self.assertContains(response, self.session1.public_cible)
        self.assertContains(response, "Il n'y a aucun participant d'inscrit pour l'instant")

    def test_with_one_register_for_session(self):
        url = reverse(URL_DETAIL_FORMATION_VIEW, args=[self.session3.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.session3.formation)
        self.assertContains(response, self.session3.formateur_id)
        self.assertContains(response, self.session3.participant_max_number)
        self.assertContains(response, self.session3.public_cible)
        self.assertContains(response, self.register3.participant.name)
        self.assertContains(response, self.register3.participant.numberFGS)
        self.assertEqual(response.context["session"], self.session3)
        self.assertEqual(response.context["session"].register_set.count(), 1)

    def test_with_many_register_not_all_for_session(self):
        url = reverse(URL_DETAIL_FORMATION_VIEW, args=[self.session2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.session2.formation)
        self.assertContains(response, self.session2.formateur_id)
        self.assertContains(response, self.session2.participant_max_number)
        self.assertContains(response, self.session2.public_cible)
        self.assertContains(response, self.register2.participant.name)
        self.assertContains(response, self.register2.participant.numberFGS)
        self.assertContains(response, self.register1.participant.name)
        self.assertContains(response, self.register1.participant.numberFGS)
        self.assertEqual(response.context["session"], self.session2)
        self.assertEqual(response.context["session"].register_set.count(), 2)

    def test_with_one_register_not_for_session(self):
        # peut-être pas a faire vu que deja fait dans test_without_register
        pass
