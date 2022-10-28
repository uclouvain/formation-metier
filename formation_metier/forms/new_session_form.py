from django.forms import ModelForm

from formation_metier.models.session import Session


class NewSessionForm(ModelForm):
    class Meta:
        model = Session
        fields = ('session_date', 'local', 'participant_max_number', 'formateur_id')
