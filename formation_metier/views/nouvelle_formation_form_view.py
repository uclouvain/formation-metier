from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import generic

from formation_metier.models.formation import Formation
from formation_metier.forms.nouvelle_formation_form import NouvelleFormationForm


class NouvelleFormationFormView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = [
        'formation_metier.add_formation',
        'formation_metier.access_to_formation_fare'
    ]
    model = Formation
    template_name = 'formation_metier/nouvelle_formation_form.html'
    form_class = NouvelleFormationForm
    success_url = '/liste_formation'
    name = 'nouvelle_formation'

    def form_valid(self, form):
        messages.success(
            self.request,
            f"La formation {form.cleaned_data['name']} a été ajouté."
        )
        return super().form_valid(form)
