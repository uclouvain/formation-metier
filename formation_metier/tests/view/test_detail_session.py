from django.contrib.auth.models import Permission, User
from django.test import TestCase

from django.urls import reverse
from django.utils import timezone

from formation_metier.enums.roles_osis_enum import ROLES_OSIS_CHOICES
from formation_metier.models.person import RoleFormationFareEnum
from formation_metier.models.seance import Seance
from formation_metier.tests.utils import create_test_formation, create_test_seance, create_test_register, \
    create_test_person, create_test_user, create_test_participant, create_test_formateur

URL_DETAIL_FORMATION_VIEW = 'formation_metier:detail_seance'


class DetailSeanceViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.date = timezone.now()
        cls.user1 = create_test_user(username="user1", password="password123")
        cls.user1.user_permissions.add(
            Permission.objects.get(codename='access_to_formation_fare'))
        cls.user1.user_permissions.add(
            Permission.objects.get(codename='view_register'))
        cls.user1.user_permissions.add(
            Permission.objects.get(codename='view_seance'))
        cls.user1 = User.objects.get(pk=cls.user1.pk)
        cls.person1 = create_test_person(name="participant1", number_fgs="XXXXX001",
                                         role_formation_metier=RoleFormationFareEnum.PARTICIPANT)
        cls.person2 = create_test_person(name="participant2", number_fgs="XXXXX002",
                                         role_formation_metier=RoleFormationFareEnum.PARTICIPANT)
        cls.person3 = create_test_person(name="participant3", number_fgs="XXXXX003",
                                         role_formation_metier=RoleFormationFareEnum.PARTICIPANT)
        cls.person4 = create_test_person(name="participant4", number_fgs="XXXXX004",
                                         role_formation_metier=RoleFormationFareEnum.PARTICIPANT)
        cls.person5 = create_test_person(name="participant5", number_fgs="XXXXX005",
                                         role_formation_metier=RoleFormationFareEnum.PARTICIPANT)
        cls.person6 = create_test_person(name="participant6", number_fgs="XXXXX006",
                                         role_formation_metier=RoleFormationFareEnum.PARTICIPANT)
        cls.person7 = create_test_person(name="formateur1", number_fgs="XXXXX007",
                                         role_formation_metier=RoleFormationFareEnum.FORMATEUR, user=cls.user1)
        cls.participant1 = create_test_participant(person=cls.person1)
        cls.participant2 = create_test_participant(person=cls.person2)
        cls.participant3 = create_test_participant(person=cls.person3)
        cls.participant4 = create_test_participant(person=cls.person4)
        cls.participant5 = create_test_participant(person=cls.person5)
        cls.participant6 = create_test_participant(person=cls.person6)
        cls.formateur1 = create_test_formateur(person=cls.person7)
        cls.formation1 = create_test_formation(name="Formation_name_1", code="AAAAA0001",
                                               public_cible=ROLES_OSIS_CHOICES[1], )
        cls.seance1 = create_test_seance(formation=cls.formation1,
                                          seance_date=cls.date,
                                          participant_max_number=10,
                                          local="L001",
                                          formateur=cls.formateur1,
                                          duree=60
                                          )
        cls.seance2 = create_test_seance(formation=cls.formation1,
                                          seance_date=cls.date,
                                          participant_max_number=5,
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
        cls.register1 = create_test_register(seance=cls.seance2,
                                             participant=cls.participant1)
        cls.register2 = create_test_register(seance=cls.seance2,
                                             participant=cls.participant2)
        cls.register3 = create_test_register(seance=cls.seance2,
                                             participant=cls.participant3)
        cls.register4 = create_test_register(seance=cls.seance2,
                                             participant=cls.participant4)
        cls.register5 = create_test_register(seance=cls.seance3,
                                             participant=cls.participant5)
        cls.register6 = create_test_register(seance=cls.seance3,
                                             participant=cls.participant6)

    def test_without_register_for_seance(self):
        self.client.force_login(user=self.user1)
        url = reverse(URL_DETAIL_FORMATION_VIEW, args=[self.seance1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.seance1.formation)
        self.assertContains(response, self.seance1.formateur)
        self.assertContains(response, self.seance1.participant_max_number)
        self.assertEqual(response.context["seance"].register_set.count(), 0)
        self.assertContains(response, "Il n'y a aucun participant d'inscrit pour l'instant")

    def test_with_many_register_not_all_for_seance(self):
        self.client.force_login(user=self.user1)
        url = reverse(URL_DETAIL_FORMATION_VIEW, args=[self.seance2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.seance2.formation)
        self.assertContains(response, self.seance2.formateur)
        self.assertContains(response, self.seance2.participant_max_number)
        self.assertContains(response, self.register2.participant.person.name)
        self.assertContains(response, self.register2.participant.person.numberFGS)
        self.assertContains(response, self.register1.participant.person.name)
        self.assertContains(response, self.register1.participant.person.numberFGS)
        self.assertContains(response, self.register3.participant.person.name)
        self.assertContains(response, self.register3.participant.person.numberFGS)
        self.assertContains(response, self.register4.participant.person.name)
        self.assertContains(response, self.register4.participant.person.numberFGS)
        self.assertNotContains(response, self.register5.participant.person.name)
        self.assertNotContains(response, self.register5.participant.person.numberFGS)
        self.assertNotContains(response, self.register6.participant.person.name)
        self.assertNotContains(response, self.register6.participant.person.numberFGS)
        self.assertEqual(response.context["seance"], self.seance2)
        self.assertEqual(response.context["seance"].register_set.count(), 4)
