from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView, FormMixin, CreateView
from formation_metier.forms.nouvelle_inscription_par_participant_form import NouvelleInscriptionParParticipantForm
from formation_metier.models.seance import Seance


class InscriptionSeancePourParticipantFormView(LoginRequiredMixin, SuccessMessageMixin,
                                               CreateView):
    template_name = 'formation_metier/inscription_seance_pour_participant.html'
    model = Seance
    context_object_name = "seance"
    pk_url_kwarg = 'seance_id'
    success_message = "Votre inscription a été sauvegardée."

    def get_form_class(self):
        form_class = NouvelleInscriptionParParticipantForm
        form_class.base_fields['participant'].initial = self.request.user.employeuclouvain
        form_class.base_fields['seance'].initial = self.get_object()
        return form_class

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'form': self.get_form(),
            'seance': self.get_object(),
        }

    def form_invalid(self, form):
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
            'formation_metier:inscription_seance',
            kwargs={
                'seance_id': self.get_object().pk
            }
        )


class InscriptionSeancePourParticipantDetailSeance(LoginRequiredMixin, FormMixin, generic.DetailView):
    model = Seance
    template_name = 'formation_metier/inscription_seance_pour_participant.html'
    context_object_name = "seance"
    pk_url_kwarg = 'seance_id'
    form_class = NouvelleInscriptionParParticipantForm

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'form': self.get_form()
        }

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['seance_id']).prefetch_related(
            'inscription_set',
        ).annotate(
            inscription_count=Count('inscription'),
        )

    def get_form_class(self):
        return NouvelleInscriptionParParticipantForm


class InscriptionSeancePourParticipantView(LoginRequiredMixin, View):
    name = 'inscription_seance'

    def get(self, request, *args, **kwargs):
        view = InscriptionSeancePourParticipantDetailSeance.as_view()
        return view(
            request,
            *args,
            **kwargs
        )

    def post(self, request, *args, **kwargs):
        view = InscriptionSeancePourParticipantFormView.as_view()
        return view(
            request,
            *args,
            **kwargs
        )
