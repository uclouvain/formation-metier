from django.db import models
from django.db.models import Q

from formation_metier.models.participant import Participant
from formation_metier.models.formateur import Formateur

from formation_metier.models.role_osis import RoleOsis


class PersonRole(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, blank=True, null=True)
    formateur = models.ForeignKey(Formateur, on_delete=models.CASCADE, blank=True, null=True)
    role_osis = models.ForeignKey(RoleOsis, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(participant__isnull=False) | Q(formateur__isnull=False),
                name='constraint_formateur_or_participant'
            )
        ]
