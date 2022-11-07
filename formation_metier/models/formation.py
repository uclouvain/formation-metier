from django.db import models
from django.db.models import UniqueConstraint


class Formation(models.Model):
    code = models.CharField(max_length=9)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    class Meta:
        constraints = [UniqueConstraint(fields=['code'], name='unique_formation_code'), ]

    def __str__(self):
        return f"{self.name}"
