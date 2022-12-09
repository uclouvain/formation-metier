from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import FormView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin

from formation_metier.forms.nouvelle_inscription_par_formateur_form import NouvelleInscriptionParFormateurForm
from formation_metier.models.seance import Seance


class InscriptionParFormateurFormView(LoginRequiredMixin, PermissionRequiredMixin, SingleObjectMixin, FormView):
    permission_required = 'formation_metier.add_inscription'
    template_name = 'formation_metier/detail_seance.html'
    form_class = NouvelleInscriptionParFormateurForm
    model = Seance
    context_object_name = "seance"
    pk_url_kwarg = 'seance_id'

    def get_form_kwargs(self):
        return {
            **super().get_form_kwargs(),
            'seance': self.get_object()
        }

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'form': self.get_form(),
            'seance': self.get_object(),
        }

    def form_valid(self, form, *args, **kwargs):
        inscription = self.get_form().save(commit=False)
        inscription.seance = self.get_object()
        inscription.save()
        messages.success(
            self.request,
            f'Le participant {inscription.participant.name} a été ajouté.'
        )
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
