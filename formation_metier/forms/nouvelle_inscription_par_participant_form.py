from django.core.exceptions import ValidationError
from django.forms import ModelForm, HiddenInput
from django.utils.translation import gettext_lazy as _

from formation_metier.models.inscription import Inscription


class NouvelleInscriptionParParticipantForm(ModelForm):
    def __init__(self, seance, *args, **kwargs):
        self.seance = seance
        super().__init__(*args, **kwargs)

    class Meta:
        model = Inscription
        fields = (
            'participant',
        )
        widgets = {
            'participant': HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        participant = cleaned_data['participant']
        if Inscription.objects.filter(seance=self.seance, participant=participant).exists():
            raise ValidationError(_(f"L'utilisateur {participant} est déja inscit à cette formation"))
        if self.seance.inscription_set.count() >= self.seance.participant_max_number:
            raise ValidationError(_("Le nombre maximal de participant inscit a cette seance est déjà atteint"))
        return cleaned_data
