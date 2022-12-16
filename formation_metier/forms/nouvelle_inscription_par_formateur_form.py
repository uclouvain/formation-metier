from pprint import pprint

from django import forms
from django.forms import ValidationError, ModelChoiceField
from django.forms import ModelForm
from django.urls import reverse
from django_select2.forms import ModelSelect2Widget
from dal import autocomplete
from django.utils.translation import gettext_lazy as _

from formation_metier.models.employe_uclouvain import EmployeUCLouvain
from formation_metier.models.inscription import Inscription


class NouvelleInscriptionParFormateurForm(ModelForm):
    seance = forms.UUIDField(
        required=False, widget=forms.HiddenInput)

    def __init__(self, seance, *args, **kwargs):
        self.seance_object = seance
        kwargs['initial'] = {'seance': seance.id}
        super().__init__(*args, **kwargs)

    class Meta:
        template_name = 'formation_metier/detail_seance.html'
        model = Inscription
        fields = (
            'participant',
        )
        widgets = {
            "participant": autocomplete.ModelSelect2(
                url='formation_metier:widget_participant',
                attrs={
                    'data-placeholder': 'Ajouter un participant',
                    'data-minimum-input-length': 3,
                    'data-html': True,
                },
                forward=['seance']
            )
        }

    def clean(self):
        pprint(self.instance)
        cleaned_data = super().clean()
        participant = cleaned_data.get('participant')
        if Inscription.objects.filter(seance=self.seance_object, participant=participant).exists():
            raise ValidationError(_(f"L'utilisateur {participant} est déja inscit à cette formation"))
        if self.seance_object.inscription_set.count() >= self.seance_object.participant_max_number:
            raise ValidationError(_("Le nombre maximal de participant inscit a cette seance est déjà atteint"))
        return cleaned_data
