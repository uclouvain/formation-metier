from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView, FormMixin
from formation_metier.forms.nouvelle_inscription_par_participant_form import NouvelleInscriptionParParticipantForm
from formation_metier.models.seance import Seance


class InscriptionSeancePourParticipantFormView(LoginRequiredMixin, SingleObjectMixin,
                                               FormView):
    template_name = 'formation_metier/inscription_seance_pour_participant.html'
    form_class = NouvelleInscriptionParParticipantForm
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

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.data._mutable = True
        form.data['participant'] = self.request.user.employeuclouvain
        form.data['seance'] = self.get_object()
        form.data._mutable = False
        return super().post(self, request, *args, **kwargs)

    def form_valid(self, form):
        inscription = self.get_form().save(commit=False)
        inscription.seance = self.get_object()
        inscription.save()
        messages.success(
            self.request,
            f"Le participant {form.data['participant'].name} a été ajouté."
        )
        return redirect(self.get_success_url())

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

    def get_form_kwargs(self):
        return {
            **super().get_form_kwargs(),
            'seance': self.get_object()
        }

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['seance_id']).prefetch_related(
            'inscription_set',
        ).annotate(
            inscription_count=Count('inscription'),
        )

    def get_form_class(self):
        return NouvelleInscriptionParParticipantForm


class InscriptionSeancePourParticipantView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'formation_metier.access_to_formation_fare'
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
