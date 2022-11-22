from django.contrib import messages
from django.db.models import Count
from django.views.generic import FormView
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from formation_metier.forms.new_registation_form import NewRegistrationForm
from formation_metier.models.session import Session


class DetailSession(FormMixin, generic.DetailView):
    model = Session
    template_name = 'formation_metier/detail_session.html'
    context_object_name = "session"
    pk_url_kwarg = 'session_id'
    form_class = NewRegistrationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get_form_kwargs(self):
        return {
            **super().get_form_kwargs(),
            'session': self.get_object()
        }

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['session_id']).prefetch_related(
            'register_set',
            'register_set__participant__person'
        ).annotate(
            register_count=Count('register'),
            )


class RegisterFormView(SingleObjectMixin, FormView):
    template_name = 'formation_metier/detail_session.html'
    form_class = NewRegistrationForm
    model = Session
    context_object_name = "session"
    pk_url_kwarg = 'session_id'

    def get_form_kwargs(self):
        return {
            **super().get_form_kwargs(),
            'session': self.get_object()
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['session'] = self.get_object()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        if self.get_form().is_valid():
            register = self.get_form().save(commit=False)
            register.session = self.get_object()
            register.save()
            messages.success(request, 'Le participant {} a été ajouté.'.format(register.participant.person.name))
        else:
            return render(request, self.template_name, {'session': self.get_object(), 'form': self.get_form()})
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('formation_metier:detail_session', kwargs={'session_id': self.get_object().pk})


class DetailSessionView(View):
    name = 'detail_session'
    def get(self, request, *args, **kwargs):
        view = DetailSession.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = RegisterFormView.as_view()
        return view(request, *args, **kwargs)
