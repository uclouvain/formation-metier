from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import DeleteView

from formation_metier.models.inscription import Inscription
from formation_metier.views import DetailSeanceView


class SuppressionUniqueInscriptionParFormateurView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = [
        'formation_metier.delete_inscription',
        'formation_metier.access_to_formation_fare'
    ]
    model = Inscription
    name = 'suppression_unique_inscriptions_par_formateur'
    pk_url_kwarg = 'inscription_id'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        seance = self.object.seance.id
        messages.success(self.request,
                         f"L'inscription de l'utilisateur : {self.object.participant.name}  a été supprimée.")
        return reverse(
            f'formation_metier:{DetailSeanceView.name}',
            kwargs={
                'seance_id': seance}
        )

