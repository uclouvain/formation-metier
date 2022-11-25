from django.core.validators import RegexValidator
from django.db import models
from django.db.models import UniqueConstraint

from formation_metier.enums.roles_osis_enum import ROLES_OSIS_CHOICES


class Formation(models.Model):
    CHOICES_PUBLIC_CIBLE = ROLES_OSIS_CHOICES
    code = models.CharField(max_length=6, blank=False,
                            validators=[RegexValidator(r'^[A-Za-z]{1,4}[0-9]{1,2}$')])
    name = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=200, blank=False)
    public_cible = models.CharField(max_length=50, choices=CHOICES_PUBLIC_CIBLE, default=None)

    class Meta:
        constraints = [UniqueConstraint(fields=['code'], name='unique_formation_code'), ]

    def __str__(self):
        return f"{self.name}"

    def get_public_cible(self) -> str:
        return self.CHOICES_PUBLIC_CIBLE[self.public_cible]
