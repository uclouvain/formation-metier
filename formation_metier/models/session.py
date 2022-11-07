import django.utils.timezone
from django.db import models

from formation_metier.models import formation


class Session(models.Model):
    ADMINISTRATEUR = 'Admin'
    FORMATEUR = 'Form'
    PARTICIPANT = 'Part'
    CHOICES_PUBLIC_CIBLE = [
        (ADMINISTRATEUR, 'Administrateurs'),
        (FORMATEUR, 'Formateurs'),
        (PARTICIPANT, 'Participant'),
    ]
    formation = models.ForeignKey(formation.Formation, on_delete=models.CASCADE)
    session_date = models.DateTimeField(default=django.utils.timezone.now)
    local = models.CharField(max_length=50)
    participant_max_number = models.IntegerField(default=0)
    formateur_id = models.CharField(max_length=50)
    public_cible = models.CharField(max_length=50, choices=CHOICES_PUBLIC_CIBLE, default=PARTICIPANT)

    def __str__(self):
        return "{} - {}".format(self.formation.name, str(self.session_date))

    def datetime_format(self):
        return self.session_date.__format__("%A %d %B %Y %Hh%I")

    def date_format(self):
        return self.session_date.__format__("%A %d %B %Y")

    def time_format(self):
        return self.session_date.__format__("%Hh%I")
