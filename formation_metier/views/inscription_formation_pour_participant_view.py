from uuid import UUID

from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin, DetailView

from formation_metier.models.formation import Formation
from formation_metier.models.inscription import Inscription


class InscriptionFormationPourParticipantForm(forms.ModelForm):
    class Meta:
        model = Inscription
        exclude = ('participant', 'seance', 'inscription_date')


class InscriptionFormationPourParticipant(LoginRequiredMixin, DetailView, SingleObjectMixin):
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
        seance_liste_apres_post = [UUID(seance) for seance in self.request.POST.getlist('seance')]
        inscriptions_existantes_liste_avant_post = Inscription.objects.filter(
            participant__user=request.user,
            seance__formation=self.get_object()
        )
        inscription_liste_a_supprimer = inscriptions_existantes_liste_avant_post.exclude(
            seance__id__in=seance_liste_apres_post)

        inscription_list_a_creer = set(seance_liste_apres_post) - set(
            inscriptions_existantes_liste_avant_post.values_list('seance_id', flat=True))

        self.delete(request, inscription_list=inscription_liste_a_supprimer)
        self.create(request, seances_liste=inscription_list_a_creer)

        return redirect(
            self.get_success_url()
        )

    def delete(self, request, inscription_list):
        for inscription in inscription_list:
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
