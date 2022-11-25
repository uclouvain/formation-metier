import django.utils.timezone
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from formation_metier.models import formation, formateur


class Seance(models.Model):
    formation = models.ForeignKey(formation.Formation, on_delete=models.CASCADE, blank=False)
    seance_date = models.DateTimeField(default=django.utils.timezone.now, blank=False)
    local = models.CharField(max_length=50, blank=False)
    participant_max_number = models.IntegerField(default=0, blank=False)
    formateur = models.ForeignKey(formateur.Formateur, on_delete=models.SET_NULL, null=True)
    duree = models.PositiveSmallIntegerField(validators=[MaxValueValidator(600)], default=60)

    class Meta:
        constraints = [UniqueConstraint(fields=['seance_date', 'local', 'formateur'], name='unique_session'), ]

    def __str__(self):
        return "{} - {}".format(self.formation.name, str(self.seance_date))

    def datetime_format(self) -> str:
        return self.seance_date.__format__("%A %d %B %Y %Hh%M")

    def time_format(self) -> str:
        return self.seance_date.__format__("%Hh%M")
