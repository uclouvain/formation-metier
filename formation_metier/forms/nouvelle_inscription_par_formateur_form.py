from django.forms import ValidationError, HiddenInput
from django.forms import ModelForm
from dal import autocomplete
from django.utils.translation import gettext_lazy as _

from formation_metier.models.inscription import Inscription


class NouvelleInscriptionParFormateurForm(ModelForm):
    seance = forms.UUIDField(
        required=False, widget=forms.HiddenInput)

    def __init__(self, seance, *args, **kwargs):
        self.seance_object = seance
        super().__init__(*args, **kwargs)

    class Meta:
        template_name = 'formation_metier/detail_seance.html'
        model = Inscription
        fields = (
            'participant',
            'seance'
        )
        widgets = {
            "participant": autocomplete.ModelSelect2(
                url='formation_metier:widget_participant',
                attrs={
                    'data-placeholder': 'Ajouter un participant',
                    'data-minimum-input-length': 3,
                    'data-html': True,
                },
            ),
            "seance": HiddenInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        participant = cleaned_data.get('participant')
        seance = cleaned_data.get('seance')
        if Inscription.objects.filter(seance=seance, participant=participant).exists():
            raise ValidationError(_(f"L'utilisateur {participant} est déja inscit à cette formation"))
        if seance.inscription_set.count() >= seance.participant_max_number:
            raise ValidationError(_("Le nombre maximal de participant inscit a cette seance est déjà atteint"))
        return cleaned_data
