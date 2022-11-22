from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views import generic

from formation_metier.models.formation import Formation


class UpdateFormationView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.edit.UpdateView):
    permission_required = 'formation_metier.change_formation'
    model = Formation
    fields = ['name', 'code', 'description']
    template_name = 'formation_metier/update_formation.html'
    pk_url_kwarg = "formation_id"
    success_message = 'La formation %(name)s a été modifiée.'
    name = 'update_formation'

    def get_success_url(self):
        return reverse('formation_metier:detail_formation', kwargs={'formation_id': self.kwargs['formation_id']})
