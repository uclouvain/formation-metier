from django.db import models
from django.db.models import UniqueConstraint

from formation_metier.enums.roles_osis_enum import ROLES_OSIS_CHOICES
from django.utils.translation import gettext_lazy as _


class Person(models.Model):
    PARTICIPANT = "PARTICIPANT"
    FORMATEUR = "FORMATEUR"
    ADMIN = "ADMIN"
    ROLES_FORMATION_FARE = (
        (PARTICIPANT, _('Participant')),
        (FORMATEUR, _('Formateur')),
        (ADMIN, _('Administrateur')),
    )

    name = models.CharField(max_length=50, blank=False)
    numberFGS = models.CharField(max_length=8, blank=False)
    role_formation_metier = models.CharField(choices=ROLES_FORMATION_FARE, max_length=50, default=None, blank=True)

    class Meta:
        constraints = [UniqueConstraint(fields=['numberFGS'], name='unique_person')]

    def __str__(self):
        return f"{self.name}"
