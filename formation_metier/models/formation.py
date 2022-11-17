from django.core.validators import RegexValidator
from django.db import models
from django.db.models import UniqueConstraint


class Formation(models.Model):
    code = models.CharField(max_length=6, blank=False,
                            validators=[RegexValidator(r'^[A-Za-z]{1,4}[0-9]{1,2}$')])
    name = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=200, blank=False)

    class Meta:
        constraints = [UniqueConstraint(fields=['code'], name='unique_formation_code'), ]

    def __str__(self):
        return f"{self.name}"
