from django.contrib import messages
from django.views import generic

from formation_metier.models.formation import Formation
from formation_metier.forms.new_formation_form import NewFormationForm


class NewFormationFormView(generic.CreateView):
    model = Formation
    template_name = 'formation_metier/new_formation_form.html'
    form_class = NewFormationForm
    success_url = '/list_formation'

    def form_valid(self, form):
        messages.success(self.request, 'La formation {} a été ajouté.'.format(form.cleaned_data['name']))
        return super().form_valid(form)
