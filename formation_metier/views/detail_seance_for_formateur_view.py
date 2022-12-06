from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django.views.generic import FormView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from formation_metier.forms.new_register_for_formateur_form import NewRegistrationForm
from formation_metier.models.seance import Seance


class DetailSeanceForFormateur(LoginRequiredMixin, PermissionRequiredMixin, FormMixin, generic.DetailView):
    permission_required = ['formation_metier.view_seance', 'formation_metier.view_register']
    model = Seance
    template_name = 'formation_metier/detail_seance.html'
    context_object_name = "seance"
    pk_url_kwarg = 'seance_id'
    form_class = NewRegistrationForm

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
            'register_set',
            'register_set__participant'
        ).annotate(
            register_count=Count('register'),
        )


class RegisterForFormateurFormView(LoginRequiredMixin, PermissionRequiredMixin, SingleObjectMixin, FormView):
    permission_required = 'formation_metier.add_register'
    template_name = 'formation_metier/detail_seance.html'
    form_class = NewRegistrationForm
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
        register = self.get_form().save(commit=False)
        register.seance = self.get_object()
        register.save()
        messages.success(self.request,
                         'Le participant {} a été ajouté.'.format(register.participant.name))
        return redirect(self.get_success_url())

    def form_invalid(self, form, *args, **kwargs):
        return render(self.request, self.template_name, {'seance': self.get_object(), 'form': self.get_form()})

    def get_success_url(self):
        return reverse('formation_metier:detail_seance', kwargs={'seance_id': self.get_object().pk})
