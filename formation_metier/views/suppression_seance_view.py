from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse
from django.views import generic

from formation_metier.models.seance import Seance


class SuppressionSeance(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    permission_required = [
        'formation_metier.delete_seance',
        'formation_metier.access_to_formation_fare'
    ]
    model = Seance
    pk_url_kwarg = "seance_id"
    name = 'suppression_seance'

    def get_success_url(self):
        messages.success(
            self.request,
            f'La seance pour la formation {self.object.formation.name} organisé le '
            f'{self.object.seance_date.__format__("%d/%m/%Y")} à {self.object.time_format()} a été supprimée.'
        )
        return reverse('formation_metier:detail_formation', kwargs={'formation_id': self.object.formation.id})
