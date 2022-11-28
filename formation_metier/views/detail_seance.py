from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django.views.generic import FormView
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from formation_metier.forms.new_registation_form import NewRegistrationForm
from formation_metier.models.seance import Seance


class DetailSeance(LoginRequiredMixin, PermissionRequiredMixin, FormMixin, generic.DetailView):
    permission_required = ('formation_metier.view_seance', 'formation_metier.view_register')
    model = Seance
    template_name = 'formation_metier/detail_seance.html'
    context_object_name = "seance"
    pk_url_kwarg = 'seance_id'
    form_class = NewRegistrationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

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


class RegisterFormView(LoginRequiredMixin, PermissionRequiredMixin, SingleObjectMixin, FormView):
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
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['seance'] = self.get_object()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        if self.get_form().is_valid():
            register = self.get_form().save(commit=False)
            register.seance = self.get_object()
            register.save()
            messages.success(request,
                             'Le participant {} a été ajouté.'.format(register.participant.name))
        else:
            return render(request, self.template_name, {'seance': self.get_object(), 'form': self.get_form()})
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('formation_metier:detail_seance', kwargs={'seance_id': self.get_object().pk})


class DetailSeanceView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'formation_metier.access_to_formation_fare'
    name = 'detail_seance'

    def get(self, request, *args, **kwargs):
        view = DetailSeance.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = RegisterFormView.as_view()
        return view(request, *args, **kwargs)
