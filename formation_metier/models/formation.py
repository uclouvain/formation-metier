from django.db import models


class Formation(models.Model):
    code = models.CharField(max_length=9)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name
