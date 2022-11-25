from django.forms import ModelForm

from formation_metier.models.seance import Seance


class NewSeanceForm(ModelForm):
    class Meta:
        model = Seance
        fields = ('seance_date', 'local', 'participant_max_number', 'formateur', 'duree')
