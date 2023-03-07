from django import forms
from django.forms import ModelForm

from formation_metier.models.seance import Seance


class NouvelleSeanceForm(ModelForm):
    seance_date = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget(
        date_attrs=({'type': 'date', "date_format": "%d/%m/%Y"}),
        time_attrs=({'type': 'time', "time_format": "%Hh%M"}),
    ))

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
