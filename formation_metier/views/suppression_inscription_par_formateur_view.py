from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import redirect

from formation_metier.models.inscription import Inscription
from django.views.generic import DeleteView


class SuppressionInscriptionParFormateur(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = [
        'formation_metier.delete_inscription',
        'formation_metier.access_to_formation_fare'
    ]
    model = Inscription
    pk_url_kwarg = "seance_id"
    name = 'suppression_inscription_par_formateur'

    def get_queryset(self):
        inscription_list = self.request.POST.getlist('inscription')
        return Inscription.objects.filter(id__in=inscription_list, seance_id=self.request.POST.get("seance_id"))

    def delete(self, request, *args, **kwargs):
        if request.method == "POST":
            inscription_list = self.get_queryset()
            seance_id = request.POST.get("seance_id")
            for inscription_object in inscription_list:
                messages.success(request, "L'inscription de l'utilisateur '{}' a été supprimée.".format(
                    inscription_object.participant.name))
            inscription_list.delete()
            return redirect('formation_metier:detail_seance', seance_id)
