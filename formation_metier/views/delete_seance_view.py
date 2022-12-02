from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views import generic

from formation_metier.models.seance import Seance


class DeleteSeance(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    permission_required = ['formation_metier.delete_seance', 'formation_metier.access_to_formation_fare']
    model = Seance
    pk_url_kwarg = "seance_id"

    def get_success_url(self):
        success_message = f'La seance pour la formation {self.object.formation.name} organisé le {self.object.seance_date.__format__("%d/%m/%Y")} à {self.object.time_format()} a été supprimée.'
        messages.success(self.request, success_message)
        return reverse('formation_metier:detail_formation', kwargs={'formation_id': self.object.formation.id})
