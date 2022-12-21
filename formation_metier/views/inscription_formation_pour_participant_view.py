from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView
from django.views.generic.detail import SingleObjectMixin

from formation_metier.models.formation import Formation
from formation_metier.models.inscription import Inscription
from formation_metier.models.seance import Seance


class InscriptionFormationPourParticipantForm(forms.ModelForm):
    class Meta:
        model = Inscription
        exclude = ('participant', 'seance', 'inscription_date')


class InscriptionFormationPourParticipant(LoginRequiredMixin, DeleteView, CreateView, SingleObjectMixin):
    model = Inscription
    pk_url_kwarg = 'formation_id'
    context_object_name = "formation"
    template_name = "formation_metier/inscription_formation_pour_participant.html"
    name = "inscription_formation"
    form_class = InscriptionFormationPourParticipantForm

    def get_queryset(self):
        return Formation.objects.filter(id=self.kwargs['formation_id']).prefetch_related(
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
        seances_liste_pour_inscription_a_creer = []
        inscriptions_liste_a_supprimer = []
        seance_list_apres_post = self.request.POST.getlist('seance')
        inscriptions_existantes_liste_avant_post = Inscription.objects.filter(
            participant__user=request.user,
            seance__formation=self.get_object()
        )
        for inscription_existante in inscriptions_existantes_liste_avant_post:
            if str(inscription_existante.seance_id) not in seance_list_apres_post:
                inscriptions_liste_a_supprimer.append(inscription_existante)
        for seance_id in seance_list_apres_post:
            if not Inscription.objects.filter(participant__user=request.user, seance__id=seance_id).exists():
                seances_liste_pour_inscription_a_creer.append(seance_id)

        if inscriptions_liste_a_supprimer:
            self.delete(request, inscriptions_liste=inscriptions_liste_a_supprimer)
        if seances_liste_pour_inscription_a_creer:
            self.create(request, seances_liste=seances_liste_pour_inscription_a_creer)
        return redirect(
            self.get_success_url()
        )

    def delete(self, request, *args, **kwargs):
        for inscription in kwargs['inscriptions_liste']:
            inscription.delete()
            messages.success(
                request,
                f"Votre inscription pour la seance du {inscription.seance.datetime_format()} a été supprimée"
            )

    def create(self, request, seances_liste):
        for seance_id in seances_liste:
            inscription_cree = Inscription.objects.create(
                participant=request.user.employeuclouvain,
                seance_id=seance_id
            )
            messages.success(
                request,
                f"Votre inscription pour la seance du {inscription_cree.seance.datetime_format()} a été sauvegardée"
            )
