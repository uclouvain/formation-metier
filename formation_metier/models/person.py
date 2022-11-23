from django.contrib.auth.models import User
from django.db import models
from django.db.models import UniqueConstraint, CheckConstraint, Q, TextChoices
from django.utils.translation import gettext_lazy as _


class RoleFormationFareEnum(TextChoices):
    PARTICIPANT = "PARTICIPANT", _('Participant')
    FORMATEUR = "FORMATEUR", _('Formateur')
    ADMIN = "ADMIN", _('Administrateur')


class Person(models.Model):
    name = models.CharField(max_length=50, blank=False)
    numberFGS = models.CharField(max_length=8, blank=False)
    role_formation_metier = models.CharField(choices=RoleFormationFareEnum.choices, max_length=50,
                                             default=RoleFormationFareEnum.PARTICIPANT, )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)

    class Meta:
        constraints = [UniqueConstraint(fields=['numberFGS'], name='unique_person'),
                       CheckConstraint(check=(Q(role_formation_metier__in=['FORMATEUR', 'ADMIN'],
                                                user__isnull=False) |
                                              Q(role_formation_metier='PARTICIPANT',
                                                user__isnull=True)),
                                       name='only_participant_have_user_null')
                       ]
        permissions = (('access_to_formation_fare', 'Global access to module formation FARE'),)

    def __str__(self):
        return f"{self.name}"
