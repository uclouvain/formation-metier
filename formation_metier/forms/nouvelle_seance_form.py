from django.forms import ModelForm

from formation_metier.models.employe_uclouvain import EmployeUCLouvain, RoleFormationFareEnum
from formation_metier.models.seance import Seance


class NouvelleSeanceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NouvelleSeanceForm, self).__init__(*args, **kwargs)
        self.fields['formateur'].queryset = EmployeUCLouvain.objects.filter(
            role_formation_metier=RoleFormationFareEnum.FORMATEUR)

    class Meta:
        model = Seance
        fields = (
            'seance_date',
            'local',
            'participant_max_number',
            'formateur',
            'duree'
        )
