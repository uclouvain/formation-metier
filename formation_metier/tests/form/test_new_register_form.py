import uuid

from django.test import TestCase
from datetime import datetime

from django.urls import reverse
from django.core.exceptions import ValidationError

from formation_metier.models.employe_uclouvain import RoleFormationFareEnum, EmployeUCLouvain
from formation_metier.models.register import Register
from formation_metier.tests.factories.employe_uclouvain import EmployeUCLouvainWithPermissionsFactory, \
    EmployeUCLouvainParticipantFactory, add_employe_uclouvain_to_groups
from formation_metier.tests.factories.register import RegisterFactory
from formation_metier.tests.factories.seance import SeanceFactory

URL_NEW_REGISTRATION = 'formation_metier:detail_seance'


class NewRegisterFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.date = datetime.today()
        cls.employe_ucl = EmployeUCLouvainWithPermissionsFactory('access_to_formation_fare', 'view_register',
                                                                 'add_register', 'view_seance',
                                                                 role=RoleFormationFareEnum.FORMATEUR)
        add_employe_uclouvain_to_groups(cls.employe_ucl, 'FromateurGroup')
        cls.employe_ucl = EmployeUCLouvain.objects.get(id=cls.employe_ucl.id)
        cls.register = RegisterFactory(participant=cls.employe_ucl, seance__participant_max_number=2)

    def test_should_authorise_access_to_formateur(self):
        self.client.force_login(user=self.employe_ucl.user)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.register.seance.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"<h2>Formation : {self.register.seance.formation.name}</h2>", html=True)
        self.assertTemplateUsed('detail_seance.html')

    def test_should_deny_access_user_case_not_logged(self):
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.register.seance.id]))
        self.assertEqual(response.status_code, 302)

    def test_should_deny_access_case_user_not_have_permission_access_to_formation_fare(self):
        employe_ucl = EmployeUCLouvainWithPermissionsFactory('view_register',
                                                             'add_register', 'view_seance')
        self.client.force_login(user=employe_ucl.user)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.register.seance.id]))
        self.assertEqual(response.status_code, 403)

    def test_should_deny_access_case_user_not_have_permission_view_seance(self):
        employe_ucl = EmployeUCLouvainWithPermissionsFactory('access_to_formation_fare', 'view_register',
                                                             'add_register')
        self.client.force_login(user=employe_ucl.user)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.register.seance.id]))
        self.assertEqual(response.status_code, 403)

    def test_should_deny_access_case_user_not_have_permission_view_register(self):
        employe_ucl = EmployeUCLouvainWithPermissionsFactory('access_to_formation_fare',
                                                             'add_register', 'view_seance')
        self.client.force_login(user=employe_ucl.user)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.register.seance.id]))
        self.assertEqual(response.status_code, 403)

    def test_should_deny_access_case_user_not_have_permission_add_register(self):
        employe_ucl = EmployeUCLouvainWithPermissionsFactory('access_to_formation_fare', 'view_register',
                                                             'view_seance')
        self.client.force_login(user=employe_ucl.user)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.register.seance.id]))
        self.assertEqual(response.status_code, 200)
        data = {"seance": self.register.seance,
                "participant": employe_ucl.id
                }
        request = self.client.post(reverse(URL_NEW_REGISTRATION, args=[self.register.seance.id]), data=data)
        self.assertEqual(request.status_code, 403)

    def test_should_add_register(self):
        seance = SeanceFactory()
        participant = EmployeUCLouvainParticipantFactory()
        self.client.force_login(user=self.employe_ucl.user)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.register.seance.id]))
        data = {
            "participant": participant
        }
        request = self.client.post(reverse(URL_NEW_REGISTRATION, args=[self.register.seance.id]), data=data, )
        test = Register.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 302)
        self.assertEqual(Register.objects.count(), 2)

    def test_should_raise_validation_error_case_register_already_exist(self):
        self.client.force_login(user=self.employe_ucl.user)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.register.seance.id]))
        data = {"seance": self.register.seance,
                "participant": self.employe_ucl.id
                }

        request = self.client.post(reverse(URL_NEW_REGISTRATION, args=[self.register.seance.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Register.objects.count(), 1)
        self.assertRaisesMessage(ValidationError,
                                 f"L'utilisateur {self.employe_ucl} est déja inscit à cette formation")

    def test_should_raise_validation_error_case_sceance_max_participant_number(self):
        participant1 = EmployeUCLouvainParticipantFactory()
        participant2 = EmployeUCLouvainParticipantFactory()
        self.client.force_login(user=self.employe_ucl.user)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.register.seance.id]))
        data1 = {
            "participant": participant1.id
        }

        data2 = {"seance": self.register.seance,
                 "participant": participant2.id
                 }
        self.assertEqual(response.status_code, 200)
        first_request = self.client.post(reverse(URL_NEW_REGISTRATION, args=[self.register.seance.id]), data=data1)
        self.assertEqual(first_request.status_code, 302)
        second_request = self.client.post(reverse(URL_NEW_REGISTRATION, args=[self.register.seance.id]), data=data2)
        self.assertEqual(second_request.status_code, 200)
        test = Register.objects.all()
        self.assertEqual(Register.objects.count(), 2)
        self.assertRaisesMessage(ValidationError,
                                 'Le nombre maximal de participant inscit a cette seance est déjà atteint')

    def test_should_raise_validation_error_case_sceance_not_exist(self):
        self.client.force_login(user=self.employe_ucl.user)
        response = self.client.get(reverse(URL_NEW_REGISTRATION, args=[self.register.seance.id]))
        data = {"seance": uuid.uuid4(),
                "participant": 19
                }
        url = reverse(URL_NEW_REGISTRATION, args=[self.register.seance_id])
        request = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Register.objects.count(), 1)
        self.assertRaises(ValueError)
