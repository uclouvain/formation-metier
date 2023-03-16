from django.forms import ModelForm

from formation_metier.models.formation import Formation


class NouvelleFormationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NouvelleFormationForm, self).__init__(*args, **kwargs)
        self.fields['code'].widget.attrs[
            'title'] = 'Le code doit être composé de maximum 4 lettres et de maximum 2 chiffres'

    class Meta:
        model = Formation
        fields = (
            'name',
            'code',
            'description',
            'public_cible'
        )
        labels = {
            'name': 'Nom de la formation'
        }
