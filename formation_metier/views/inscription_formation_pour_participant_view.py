from uuid import UUID

from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView
from django.views.generic.detail import SingleObjectMixin

from formation_metier.models.formation import Formation
from formation_metier.models.inscription import Inscription


class InscriptionFormationPourParticipantForm(forms.ModelForm):
    class Meta:
        model = Inscription
        exclude = ('participant', 'seance', 'inscription_date')


class InscriptionFormationPourParticipant(LoginRequiredMixin, CreateView, DeleteView, SingleObjectMixin):
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
        seance_list_apres_post = self.request.POST.getlist('seance')
        seance_uuid_list_apres_post = []
        for seance in seance_list_apres_post:
            seance_uuid_list_apres_post.append(UUID(seance))
        inscriptions_existantes_liste_avant_post = Inscription.objects.filter(
            participant__user=request.user,
            seance__formation=self.get_object()
        )
        seance_to_delete = inscriptions_existantes_liste_avant_post.exclude(seance__id__in=seance_uuid_list_apres_post)
        seance_to_create = set(seance_uuid_list_apres_post) - set(
            inscriptions_existantes_liste_avant_post.values_list('seance_id', flat=True))

        self.delete(request, seance_to_delete)
        self.create(request, seance_to_create)

        return redirect(
            self.get_success_url()
        )

    def delete(self, request, to_delete):
        for inscription in to_delete:
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
