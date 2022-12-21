from django.core.exceptions import ValidationError
from django.forms import ModelForm, HiddenInput
from django.utils.translation import gettext_lazy as _

from formation_metier.models.inscription import Inscription


class NouvelleInscriptionParParticipantForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['participant'].required = False
        self.fields['seance'].required = False

    class Meta:
        model = Inscription
        fields = (
            'participant',
            'seance',
        )
        widgets = {
            'participant': HiddenInput(),
            'seance': HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['seance'] = self.fields['seance'].initial
        cleaned_data['participant'] = self.fields['participant'].initial
        if Inscription.objects.filter(seance=cleaned_data['seance'], participant=cleaned_data['participant']).exists():
            raise ValidationError(_(f"L'utilisateur {cleaned_data['participant']} est déja inscit à cette formation"))
        if cleaned_data['seance'].inscription_set.count() >= cleaned_data['seance'].participant_max_number:
            raise ValidationError(_("Le nombre maximal de participant inscit a cette seance est déjà atteint"))
        return cleaned_data
