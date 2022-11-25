from django.forms import ModelForm

from formation_metier.models.formation import Formation


class NewFormationForm(ModelForm):
    class Meta:
        model = Formation
        fields = ('name', 'code', 'description', 'public_cible')

    # A voir si Charfield convertis automatiquement en Str
    def clean_name(self):
        data = self.cleaned_data['name']
        if type(data) != str:
            raise TypeError("Le nom de la formation doit être de type str")
        return data

    def clean_code(self):
        data = self.cleaned_data['code']
        if type(data) != str:
            raise TypeError("Le code de la formation doit être de type str")
        return data

    def clean_description(self):
        data = self.cleaned_data['description']
        if type(data) != str:
            raise TypeError("La description de la formation doit être de type str")
        return data
