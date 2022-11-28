import django.utils.timezone
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint, CheckConstraint, Q
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from formation_metier.models import formation, employe_uclouvain
from formation_metier.models.employe_uclouvain import EmployeUCLouvain


def validate_formateur(formateur_id):
    employe_ucl = EmployeUCLouvain.objects.get(id=formateur_id)
    if employe_ucl.role_formation_metier != employe_uclouvain.RoleFormationFareEnum.FORMATEUR:
        raise ValidationError(
            _("%(formateur)s n'est pas un formateur du module : 'formation FARE'"),
            params={'formateur': employe_ucl},
        )


class Seance(models.Model):
    formation = models.ForeignKey(formation.Formation, on_delete=models.CASCADE, blank=False)
    seance_date = models.DateTimeField(default=django.utils.timezone.now, blank=False)
    local = models.CharField(max_length=50, blank=False)
    participant_max_number = models.PositiveSmallIntegerField(default=0, blank=False)
    formateur = models.ForeignKey(employe_uclouvain.EmployeUCLouvain, on_delete=models.SET_NULL, null=True,
                                  validators=[validate_formateur])
    duree = models.PositiveSmallIntegerField(validators=[MaxValueValidator(600)], default=60)

    class Meta:
        constraints = [UniqueConstraint(fields=['seance_date', 'local', 'formateur'], name='unique_session'),
                       ]

    def __str__(self):
        return "{} - {}".format(self.formation.name, str(self.seance_date))

    def datetime_format(self) -> str:
        return self.seance_date.__format__("%A %d %B %Y %Hh%M")

    def time_format(self) -> str:
        return self.seance_date.__format__("%Hh%M")
