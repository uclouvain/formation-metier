from django.forms import ModelForm

from formation_metier.models.formation import Formation


class NouvelleFormationForm(ModelForm):
    class Meta:
        model = Formation
        fields = (
            'name',
            'code',
            'description',
            'public_cible'
        )
