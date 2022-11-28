from django.contrib.auth.models import User
from django.db import models
from django.db.models import UniqueConstraint, CheckConstraint, Q, TextChoices
from django.utils.translation import gettext_lazy as _


class RoleFormationFareEnum(TextChoices):
    PARTICIPANT = "PARTICIPANT", _('Participant')
    FORMATEUR = "FORMATEUR", _('Formateur')
    ADMIN = "ADMIN", _('Administrateur')


class EmployeUCLouvain(models.Model):
    name = models.CharField(max_length=50, blank=False)
    numberFGS = models.CharField(max_length=8, blank=False)
    role_formation_metier = models.CharField(choices=RoleFormationFareEnum.choices, max_length=50,
                                             default=RoleFormationFareEnum.PARTICIPANT, )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    class Meta:
        constraints = [UniqueConstraint(fields=['numberFGS'], name='unique_person')]
        permissions = (('access_to_formation_fare', 'Global access to module formation FARE'),)

    def __str__(self):
        return f"{self.name}"
