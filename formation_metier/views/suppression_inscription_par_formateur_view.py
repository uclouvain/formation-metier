from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from formation_metier.models.inscription import Inscription
from django.views.generic import DeleteView
from formation_metier.views import DetailSeanceView


class SuppressionInscriptionParFormateur(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = [
        'formation_metier.delete_inscription',
        'formation_metier.access_to_formation_fare'
    ]
    model = Inscription
    name = 'suppression_inscription_par_formateur'

    def get_queryset(self):
        inscription_list = self.request.POST.getlist('inscription')
        return Inscription.objects.filter(id__in=inscription_list, seance_id=self.request.POST.get("seance_id"))

    def get_success_url(self):
        inscription_list = self.get_queryset()
        for inscription_object in inscription_list:
            messages.success(
                self.request,
                f"L'inscription de l'utilisateur '{inscription_object.participant.name}' a été supprimée."
            )
        seance = self.request.POST.get("seance_id")
        return reverse(
            f'formation_metier:{DetailSeanceView.name}',
            kwargs={
                'seance_id': seance}
        )

    def delete(self, request, *args, **kwargs):
        self.get_queryset().delete()
        return redirect(self.get_success_url())

