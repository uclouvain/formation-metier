from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from formation_metier.models.formation import Formation
from formation_metier.models.seance import Seance
from formation_metier.forms.nouvelle_seance_form import NouvelleSeanceForm


class NouvelleSeanceFormView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = [
        'formation_metier.add_seance',
        'formation_metier.access_to_formation_fare'
    ]
    model = Seance
    template_name = 'formation_metier/nouvelle_seance_form.html'
    form_class = NouvelleSeanceForm
    pk_url_kwarg = "formation_id"
    name = 'nouvelle_seance'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formation_id"] = self.kwargs['formation_id']
        return context

    def get_success_url(self):
        return reverse(
            'formation_metier:detail_formation',
            kwargs={'formation_id': self.kwargs['formation_id']}
        )

    def form_valid(self, form):
        formation_object = get_object_or_404(Formation, id=self.kwargs['formation_id'])
        form.instance.formation = formation_object
        messages.success(
            self.request,
            f"La seance du {form.cleaned_data['seance_date'].__format__('%d/%m/%Y')}"
            f" à {form.cleaned_data['seance_date'].__format__('%Hh%M')} a été ajouté."
        )
        return super().form_valid(form)
