from django.db import models
from formation_metier.models.person import Person


class Formateur(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.person.name
