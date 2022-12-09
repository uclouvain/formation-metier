import uuid

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.db.models import UniqueConstraint, TextChoices
from django.utils.translation import gettext_lazy as _


class RoleFormationFareEnum(TextChoices):
    PARTICIPANT = "PARTICIPANT", _('Participant')
    FORMATEUR = "FORMATEUR", _('Formateur')
    ADMIN = "ADMIN", _('Administrateur')


MAX_LENGTH_NAME = 50
MAX_LENGTH_MATRICULE_FGS = 8
MAX_LENGTH_DESCRIPTION = 200
MAX_LENGTH_ROLE_FORMATION_METIER = 200


class EmployeUCLouvain(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        blank=False
    )
    number_fgs = models.CharField(
        max_length=MAX_LENGTH_MATRICULE_FGS,
        blank=False
    )
    role_formation_metier = models.CharField(
        choices=RoleFormationFareEnum.choices,
        max_length=MAX_LENGTH_ROLE_FORMATION_METIER,
        default=RoleFormationFareEnum.PARTICIPANT,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['number_fgs'], name='unique_person')
        ]
        permissions = [
            ('access_to_formation_fare', 'Global access to module formation FARE'),
            ('suppression_inscription_par_participant', 'Can delete self inscription'),
        ]

    def __str__(self):
        return f"{self.name}"


class EmployeUCLouvainAdmin(admin.ModelAdmin):
    search_fields = ['name']
    fieldsets = [
        ('name', {'fields': ['name']}),
        ('number_fgs', {'fields': ['number_fgs']}),
        ('role_formation_metier', {'fields': ['role_formation_metier']}),
        ('user', {'fields': ['user']}),
    ]
    list_display = (
        'name',
        'number_fgs',
        'role_formation_metier',
        'user'
    )
