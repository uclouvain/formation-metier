from django.db import models

from formation_metier.models.person import Person


class Participant(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=False)
