import django.utils.timezone
from django.db import models

from formation_metier.models import formation


class Session(models.Model):
    formation = models.ForeignKey(formation.Formation, on_delete=models.CASCADE)
    session_date = models.DateTimeField(default=django.utils.timezone.now)
    local = models.CharField(max_length=50)
    participant_max_number = models.IntegerField(default=0)
    formateur_id = models.CharField(max_length=50)
