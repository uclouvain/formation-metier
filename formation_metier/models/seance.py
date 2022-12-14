import math
import uuid
from datetime import timedelta

import django.utils.timezone
from django.contrib import admin
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from formation_metier.models import formation
from formation_metier.models.employe_uclouvain import EmployeUCLouvain, RoleFormationFareEnum


def validate_formateur(formateur_id):
    employe_ucl = EmployeUCLouvain.objects.get(id=formateur_id)
    if employe_ucl.role_formation_metier != RoleFormationFareEnum.FORMATEUR:
        raise ValidationError(
            _("%(formateur)s n'est pas un formateur du module : 'formation FARE'"),
            params={'formateur': employe_ucl},
        )


DEFAULT_DUREE = 60
DEFAULT_PARTICIPANT_NUMBER = 20
MAX_DUREE = 600
MAX_LENGTH_LOCAL = 50


class Seance(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    formation = models.ForeignKey(
        formation.Formation,
        on_delete=models.CASCADE,
        blank=False)
    seance_date = models.DateTimeField(
        default=django.utils.timezone.now,
        blank=False)
    local = models.CharField(
        max_length=MAX_LENGTH_LOCAL,
        blank=False)
    participant_max_number = models.PositiveSmallIntegerField(
        default=DEFAULT_PARTICIPANT_NUMBER,
        blank=False)
    formateur = models.ForeignKey(
        EmployeUCLouvain,
        on_delete=models.SET_NULL,
        null=True,
        validators=[validate_formateur])
    duree = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(MAX_DUREE)],
        default=DEFAULT_DUREE)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=[
                    'seance_date',
                    'local',
                    'formateur'
                ],
                name='unique_session'
            ),
        ]

    def __str__(self):
        return "{} - {}".format(self.formation.name, str(self.seance_date))

    def datetime_format(self) -> str:
        return self.seance_date.__format__("%x à %Hh%M")

    def time_format(self) -> str:
        return self.seance_date.__format__("%Hh%M")

    def duree_en_heure(self) -> str:
        duree_calcule_en_heure = math.modf(self.duree / 60)
        if duree_calcule_en_heure[0] == 0.0:
            return str(int(duree_calcule_en_heure[1])) + " h"
        else:
            duree_minutes = self.duree - (60 * int(duree_calcule_en_heure[1]))
            if duree_minutes > 9:
                return str(int(duree_calcule_en_heure[1])) + " h " + str(duree_minutes)
            else:
                return str(int(duree_calcule_en_heure[1])) + " h 0" + str(duree_minutes)


class SeanceAdmin(admin.ModelAdmin):
    fieldsets = [
        ('formation', {'fields': ['formation']}),
        ('seance_date', {'fields': ['seance_date']}),
        ('local', {'fields': ['local']}),
        ('participant_max_number', {'fields': ['participant_max_number']}),
        ('formateur', {'fields': ['formateur']}),
        ('duree', {'fields': ['duree']})
    ]
    list_display = (
        'id',
        'formation',
        'seance_date',
        'local',
        'participant_max_number',
        'formateur',
        'duree'
    )


class SeanceInLine(admin.StackedInline):
    model = Seance
    extra = 3
