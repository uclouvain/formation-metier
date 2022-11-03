from django.db import models


class Person(models.Model):
    ROLES = [('admin', "admin"), ('formateur', 'formateur'), ('participant', 'participant'), ]
    name = models.CharField(max_length=50)
    numberFGS = models.CharField(max_length=8)
    role = models.CharField(choices=ROLES, max_length=20)

    def __str__(self):
        return self.name
