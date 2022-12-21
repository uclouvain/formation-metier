from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DeleteView

from formation_metier.models.inscription import Inscription


class SuppressionInscriptionParParticipant(LoginRequiredMixin, DeleteView):
    model = Inscription
    name = 'suppression_inscription_par_participant'

    def get_object(self, queryset=None):
        inscription = Inscription.objects.get(
            participant_id=self.request.user.employeuclouvain.id,
            seance_id=self.request.POST.get('seance_id')
        )
        return inscription

    def get_success_url(self):
        inscription = self.get_object()
        messages.success(self.request,
                         f"Votre inscription à la seance du {inscription.seance.seance_date.date()} pour la formation '{inscription.seance.formation}'  a été supprimée.")
        return reverse(
            'formation_metier:inscription_seance',
            kwargs={
                'seance_id': inscription.seance_id}
        )
