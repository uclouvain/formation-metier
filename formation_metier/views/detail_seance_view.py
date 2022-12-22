from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count, Prefetch
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.detail import SingleObjectMixin

from formation_metier.forms.nouvelle_inscription_par_formateur_form import NouvelleInscriptionParFormateurForm
from formation_metier.models.inscription import Inscription
from formation_metier.models.seance import Seance


class DetailSeanceView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView, SingleObjectMixin):
    permission_required = [
        'formation_metier.view_seance',
        'formation_metier.view_inscription',
        'formation_metier.access_to_formation_fare'
    ]
    name = 'detail_seance'
    model = Inscription
    template_name = 'formation_metier/detail_seance.html'
    context_object_name = "seance"
    pk_url_kwarg = 'seance_id'

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'form': self.get_form(),
            'seance': self.get_object()
        }

    def get_form_kwargs(self):
        return {
            **super().get_form_kwargs(),
            'seance': self.get_object()
        }

    def get_queryset(self):
        return Seance.objects.filter(
            id=self.kwargs['seance_id']
        ).prefetch_related(
            Prefetch(
                'inscription_set',
                queryset=Inscription.objects.order_by('participant')
            ),
        ).annotate(
            inscription_count=Count('inscription'),
        )

    def get_form_class(self):
        form_class = NouvelleInscriptionParFormateurForm
        form_class.base_fields['seance'].initial = self.get_object()
        return form_class

    def form_valid(self, form):
        participant = form.cleaned_data['participant']
        seance = form.cleaned_data['seance']
        messages.success(
            self.request,
            f'Le participant {participant} a été ajouté.'
        )
        Inscription.objects.create(participant=participant, seance=seance)
        return redirect(self.get_success_url())

    def form_invalid(self, form, *args, **kwargs):
        return render(
            self.request,
            self.template_name,
            {
                'seance': self.get_object(),
                'form': self.get_form()
            }
        )

    def get_success_url(self):
        return reverse(
            'formation_metier:detail_seance',
            kwargs={
                'seance_id': self.get_object().pk
            }
        )
