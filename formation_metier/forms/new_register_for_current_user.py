from django.forms import ModelForm

from formation_metier.models.register import Register


class NewRegisterForCurrentUser(ModelForm):
    class Meta:
        model = Register
        exclude = ('seance', 'participant', 'register_date')
