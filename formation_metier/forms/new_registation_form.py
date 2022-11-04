from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django_select2.forms import ModelSelect2Widget
from dal import autocomplete
from django.utils.translation import gettext_lazy as _

from formation_metier.models.person import Person
from formation_metier.models.register import Register


class NewRegistrationParticipantWidget(ModelSelect2Widget):
    model = Person
    search_fields = ["name__icontains"]


class NewRegistrationForm(ModelForm):
    class Meta:
        template_name = 'formation_metier/detail_session.html'
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

    def clean_session(self, session, participant):
        register_set = session.register_set.all()
        for register in register_set:
            if register.participant == participant:
                raise ValidationError(_('Vous êtes déja inscit a cette formation'))
        if session.participant_max_number <= register_set.count():
            raise ValidationError(_("Le nombre maximal de participant inscit a cette formation est déjà atteint"))
        return self.cleaned_data.get('session')
