from django.conf.urls import url
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
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

    def get_success_url(self):
        return reverse('formation_metier:detail_session', kwargs={'session_id': self.kwargs['session_id']})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return render(request, self.template_name, {'errors': form.errors, 'form': form})

    def form_valid(self, form):
        participant = form.cleaned_data.get("participant")
        session = self.get_object()
        # form.clean_session(session, participant)
        Register.objects.create(participant=participant, session=session)
        return super(DetailSession, self).form_valid(form)

    def form_invalid(self, form):
        # put logic here
        return super(DetailSession, self).form_invalid(form)

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['session_id']).prefetch_related(
            'register_set',
        )
