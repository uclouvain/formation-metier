from datetime import datetime
from uuid import UUID

from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef, Prefetch
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
        date = datetime.now()
        seance_qs = Seance.objects.filter(
            formation_id=self.kwargs['formation_id']
        ).order_by(
            'seance_date'
        ).prefetch_related(
            'inscription_set'
        ).annotate(
            est_inscrit_seance=Exists(
                Inscription.objects.filter(
                    participant=self.request.user.employeuclouvain,
                    seance=OuterRef('pk')
                )
            ),
            est_seance_passee=Exists(
                Seance.objects.filter(
                    seance_date__lt=date,
                    id=OuterRef('pk')
                ),
            )
        )
        return super().get_queryset().prefetch_related(
            Prefetch(
                'seance_set',
                queryset=seance_qs
            ),
        ).annotate(
            est_inscrit_formation=Exists(
                Inscription.objects.filter(
                    participant=self.request.user.employeuclouvain,
                    seance__formation=OuterRef('pk')
                )
            ),
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
            seance_list_apres_post = self.request.POST.getlist('seance')
            for inscription_existante in inscriptions_existantes_avant_post:
                if str(inscription_existante.seance.id) not in seance_list_apres_post and inscription_existante.seance.seance_date > datetime.datetime.now():
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