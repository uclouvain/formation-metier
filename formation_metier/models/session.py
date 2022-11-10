import django.utils.timezone
from django.db import models

from formation_metier.models import formation
from formation_metier.models.person import Person


class Session(models.Model):

    CHOICES_PUBLIC_CIBLE = Person.ROLES
    formation = models.ForeignKey(formation.Formation, on_delete=models.CASCADE, blank=False)
    session_date = models.DateTimeField(default=django.utils.timezone.now, blank=False)
    local = models.CharField(max_length=50, blank=False)
    participant_max_number = models.IntegerField(default=0, blank=False)
    formateur_id = models.CharField(max_length=50, blank=False)
    public_cible = models.CharField(max_length=50, choices=CHOICES_PUBLIC_CIBLE, default=Person.PARTICIPANT)

    def __str__(self):
        return "{} - {}".format(self.formation.name, str(self.session_date))

    def datetime_format(self):
        return self.session_date.__format__("%A %d %B %Y %Hh%I")

    def date_format(self):
        return self.session_date.__format__("%A %d %B %Y")

    def time_format(self):
        return self.session_date.__format__("%Hh%I")
