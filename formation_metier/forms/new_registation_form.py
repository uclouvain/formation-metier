from django.forms import ModelForm
from django_select2.forms import ModelSelect2Widget
from dal import autocomplete

from formation_metier.models.person import Person
from formation_metier.models.register import Register


class NewRegistrationParticipantWidget(ModelSelect2Widget):
    model = Person
    search_fields = ["name__icontains"]


class NewRegistrationForm(ModelForm):
    class Meta:
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
