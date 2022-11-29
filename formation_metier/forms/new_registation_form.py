from django.db import IntegrityError
from django.forms import ValidationError
from django.forms import ModelForm
from django_select2.forms import ModelSelect2Widget
from dal import autocomplete
from django.utils.translation import gettext_lazy as _

from formation_metier.models.employe_uclouvain import EmployeUCLouvain
from formation_metier.models.register import Register


class NewRegistrationParticipantWidget(ModelSelect2Widget):
    model = EmployeUCLouvain
    search_fields = ["name__icontains"]


class NewRegistrationForm(ModelForm):
    def __init__(self, seance, *args, **kwargs):
        self.seance = seance
        super().__init__(*args, **kwargs)

    class Meta:
        template_name = 'formation_metier/detail_seance.html'
        model = Register
        fields = ('participant',)
        widgets = {
            "participant": autocomplete.ModelSelect2(url='formation_metier:widget_participant',
                                                     attrs={
                                                         'data-placeholder': 'Ajouter un participant',
                                                         'data-minimum-input-length': 1,
                                                         'data-html': True},
                                                     )
        }

    def clean(self):
        cleaned_data = super().clean()
        particpant = cleaned_data.get('participant')
        if Register.objects.filter(seance=self.seance, participant=particpant).exists():
            raise IntegrityError(_(f"L'utilisateur {particpant} est déja inscit à cette formation"))
        if self.seance.participant_max_number <= Register.objects.count():
            raise ValidationError(_("Le nombre maximal de participant inscit a cette seance est déjà atteint"))
        return cleaned_data
