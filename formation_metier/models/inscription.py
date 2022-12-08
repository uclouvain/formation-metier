import uuid

from django.contrib import admin
from django.db import models

from formation_metier.models.employe_uclouvain import EmployeUCLouvain
from formation_metier.models.seance import Seance


class Inscription(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, blank=False)
    participant = models.ForeignKey(EmployeUCLouvain, on_delete=models.CASCADE, blank=False)
    inscription_date = models.DateTimeField(auto_now_add=True, blank=False)

    class Meta:
        unique_together = ('seance', 'participant',)


class InscriptionAdmin(admin.ModelAdmin):
    fieldsets = [('seance', {'fields': ['seance']}),
                 ('participant', {'fields': ['participant']}),
                 ]
    list_display = ('seance', 'participant', 'inscription_date')
