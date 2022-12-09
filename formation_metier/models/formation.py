import uuid

from django.contrib import admin
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import UniqueConstraint

from formation_metier.enums.roles_osis_enum import ROLES_OSIS_CHOICES

MAX_LENGTH_CODE = 6
MAX_LENGTH_NAME = 50
MAX_LENGTH_DESCRIPTION = 200
MAX_LENGTH_PUBLIC_CIBLE = 200


class Formation(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    code = models.CharField(
        max_length=MAX_LENGTH_CODE,
        blank=False,
        validators=[
            RegexValidator(r'^[A-Za-z]{1,4}[0-9]{1,2}$')
        ]
    )
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        blank=False
    )
    description = models.CharField(
        max_length=MAX_LENGTH_DESCRIPTION,
        blank=False
    )
    public_cible = models.CharField(
        max_length=MAX_LENGTH_PUBLIC_CIBLE,
        choices=ROLES_OSIS_CHOICES,
        default=None
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['code'], name='unique_formation_code'),
        ]

    def __str__(self):
        return f"{self.name}"


class FormationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('code', {'fields': ['code']}),
        ('name', {'fields': ['name']}),
        ('description', {'fields': ['description']}),
        ('public_cible', {'fields': ['public_cible']})
    ]
    list_display = (
        'name',
        'code',
        'description',
        'public_cible'
    )
