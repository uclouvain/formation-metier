from django.views.generic import FormView
from django.conf.urls import url
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.views import generic, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from formation_metier.forms.new_registation_form import NewRegistrationForm
from formation_metier.models.register import Register
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

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['session_id']).prefetch_related(
            'register_set',
        )


class RegisterFormView(SingleObjectMixin, FormView):
    template_name = 'formation_metier/detail_session.html'
    form_class = NewRegistrationForm
    model = Session
    context_object_name = "session"
    pk_url_kwarg = 'session_id'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('formation_metier:detail_session', kwargs={'session_id': self.object.pk})

    def form_valid(self, form):
        participant = form.cleaned_data.get("participant")
        session = self.get_object()
        form.clean_session(session, participant)
        Register.objects.create(participant=participant, session=session)
        messages.success(self.request, "l'inscription a été bien enregistrée")
        return super().form_valid(form)


class DetailSessionView(View):
    def get(self, request, *args, **kwargs):
        view = DetailSession.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = RegisterFormView.as_view()
        return view(request, *args, **kwargs)
