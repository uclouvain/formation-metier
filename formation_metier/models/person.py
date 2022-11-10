from django.db import models


class Person(models.Model):
    ADMINISTRATEUR = 'Admin'
    FORMATEUR = 'Form'
    PARTICIPANT = 'Part'
    ROLES = [
        (ADMINISTRATEUR, 'Administrateurs'),
        (FORMATEUR, 'Formateurs'),
        (PARTICIPANT, 'Participant'),
    ]
    name = models.CharField(max_length=50, blank=False)
    numberFGS = models.CharField(max_length=8, blank=False)
    role_formation_metier = models.CharField(choices=ROLES, max_length=20, default=PARTICIPANT,blank=False)

    def __str__(self):
        return f"{self.name}"
