from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import generic

from formation_metier.models.formation import Formation
from formation_metier.forms.new_formation_form import NewFormationForm


class NewFormationFormView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = ['formation_metier.add_formation', 'formation_metier.access_to_formation_fare']
    model = Formation
    template_name = 'formation_metier/new_formation_form.html'
    form_class = NewFormationForm
    success_url = '/list_formation'
    name = 'new_formation'

    def form_valid(self, form):
        messages.success(self.request, 'La formation {} a été ajouté.'.format(form.cleaned_data['name']))
        return super().form_valid(form)
