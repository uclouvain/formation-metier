from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views import generic

from formation_metier.models.seance import Seance


class UpdateSeanceView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.edit.UpdateView):
    permission_required = ['formation_metier.change_seance', 'formation_metier.access_to_formation_fare']
    model = Seance
    fields = ['seance_date', 'local', 'participant_max_number', 'formateur', 'duree']
    template_name = 'formation_metier/update_seance.html'
    pk_url_kwarg = "seance_id"
    success_message = 'La seance a été modifiée.'
    name = 'update_seance'

    def get_success_url(self):
        return reverse('formation_metier:detail_seance', kwargs={'seance_id': self.kwargs['seance_id']})
