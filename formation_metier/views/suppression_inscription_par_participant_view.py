from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DeleteView

from formation_metier.models.inscription import Inscription


class SuppressionInscriptionParParticipant(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = [
        'formation_metier.suppression_inscription_par_participant',
        'formation_metier.access_to_formation_fare'
    ]
    model = Inscription
    name = 'suppression_inscription_par_participant'

    def get_queryset(self):
        self.request.POST.get('seance_id')
        inscription = Inscription.objects.get(
            participant=self.request.user.employeuclouvain,
            seance_id=self.request.POST.get("seance_id")
        )
        return inscription

    def delete(self, request, *args, **kwargs):
        if request.method == "POST":
            inscription = self.get_queryset()
            if inscription is None:
                raise AssertionError("Vous n'êtes pas inscrit à cette seance")
            else:
                seance_id = request.POST.get("seance_id")
                messages.success(request,
                                 f"Votre inscription à la seance du {inscription.seance.seance_date.date()} pour la formation '{inscription.seance.formation}'  a été supprimée.")
                inscription.delete()
            return redirect(
                'formation_metier:inscription_seance',
                seance_id
            )
