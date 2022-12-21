
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import generic

from formation_metier.models.formation import Formation


class SuppressionFormation(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    permission_required = [
        'formation_metier.delete_formation',
        'formation_metier.access_to_formation_fare'
    ]
    model = Formation
    pk_url_kwarg = "formation_id"
    name = 'suppression_formation'

    def get_success_url(self):
        messages.success(
            self.request,
            f'La formation {self.object.name} a été supprimée.'
        )
        return '/liste_formations'
