import django.utils.timezone
from django.core.validators import MaxValueValidator
from django.db import models

from formation_metier.models import formation, formateur
from formation_metier.enums.roles_osis_enum import ROLES_OSIS_CHOICES


class Session(models.Model):
    CHOICES_PUBLIC_CIBLE = ROLES_OSIS_CHOICES
    formation = models.ForeignKey(formation.Formation, on_delete=models.CASCADE, blank=False)
    session_date = models.DateTimeField(default=django.utils.timezone.now, blank=False)
    local = models.CharField(max_length=50, blank=False)
    participant_max_number = models.IntegerField(default=0, blank=False)
    formateur = models.ForeignKey(formateur.Formateur, on_delete=models.SET_NULL, null=True)
    public_cible = models.CharField(max_length=50, choices=CHOICES_PUBLIC_CIBLE, default=None)
    duree = models.PositiveSmallIntegerField(validators=[MaxValueValidator(600)], default=60)

    def __str__(self):
        return "{} - {}".format(self.formation.name, str(self.session_date))

    def datetime_format(self) -> str:
        return self.session_date.__format__("%A %d %B %Y %Hh%I")

    def date_format(self) -> str:
        return self.session_date.__format__("%A %d %B %Y")

    def time_format(self) -> str:
        return self.session_date.__format__("%Hh%I")

    def get_public_cible(self) -> str:
        return self.CHOICES_PUBLIC_CIBLE[self.public_cible]
