from django.forms import ModelForm

from formation_metier.models.register import Register


class NewRegistrationForm(ModelForm):
    class Meta:
        model = Register
        fields = ('participant',)
