from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic

from formation_metier.models.formation import Formation


class UpdateFormationView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Formation
    fields = ['name', 'code', 'description']
    template_name = 'formation_metier/update_formation.html'
    pk_url_kwarg = "formation_id"

    def get_success_url(self):
        return reverse('formation_metier:detail_formation', kwargs={'formation_id': self.kwargs['formation_id']})
