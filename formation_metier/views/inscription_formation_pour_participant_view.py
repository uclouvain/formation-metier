from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from formation_metier.models.formation import Formation
from formation_metier.models.inscription import Inscription
from formation_metier.models.seance import Seance


class InscriptionAUneFormation(LoginRequiredMixin, generic.DetailView):
    model = Formation
    pk_url_kwarg = 'formation_id'
    context_object_name = "formation"
    template_name = "formation_metier/inscription_formation_pour_participant.html"
    name = "inscription_formation"

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['formation_id']).prefetch_related(
            'seance_set',
            'seance_set__inscription_set',
        )

    def get_success_url(self):
        return reverse(
            'formation_metier:inscription_formation',
            kwargs={
                'formation_id': self.get_object().id
            }
        )

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            inscriptions_existantes_avant_post = Inscription.objects.filter(
                participant__user=request.user,
                seance__formation=self.get_object()
            )
            seance_list_apres_post = self.request.POST.getlist('seance')
            for inscription_existante in inscriptions_existantes_avant_post:
                if str(inscription_existante.seance.id) not in seance_list_apres_post:
                    inscription_existante.delete()
                    messages.success(
                        request,
                        f"Votre inscription pour la seance du {inscription_existante.seance.datetime_format()} a été supprimée"
                    )
            for seance_id in seance_list_apres_post:
                if not Inscription.objects.filter(participant__user=request.user, seance_id=seance_id).exists():
                    seance_object = Seance.objects.get(id=seance_id)
                    inscription_cree = Inscription.objects.create(
                        participant=request.user.employeuclouvain,
                        seance=seance_object
                    )
                    messages.success(
                        request,
                        f"Votre inscription pour la seance du {inscription_cree.seance.datetime_format()} a été sauvegardée"
                    )
            return redirect(
                self.get_success_url()
            )
