from django.forms import ModelForm

from formation_metier.models.seance import Seance


class NouvelleSeanceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NouvelleSeanceForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Seance
        fields = (
            'seance_date',
            'local',
            'participant_max_number',
            'formateur',
            'duree'
        )
