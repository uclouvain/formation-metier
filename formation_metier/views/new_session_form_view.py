from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from formation_metier.models.formation import Formation
from formation_metier.models.session import Session
from formation_metier.forms.new_session_form import NewSessionForm


class NewSessionFormView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = ['formation_metier.add_session', 'formation_metier.access_to_formation_fare']
    model = Session
    template_name = 'formation_metier/new_session_form.html'
    form_class = NewSessionForm
    pk_url_kwarg = "formation_id"
    name = 'new_session'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formation_id"] = self.kwargs['formation_id']
        return context

    def get_success_url(self):
        return reverse('formation_metier:detail_formation', kwargs={'formation_id': self.kwargs['formation_id']})

    def form_valid(self, form):
        formation = get_object_or_404(Formation, id=self.kwargs['formation_id'])
        form.instance.formation = formation
        messages.success(self.request, 'La session du {} à {} a été ajouté.'.format(
            form.cleaned_data['session_date'].__format__("%A %d %B %Y"),
            form.cleaned_data['session_date'].__format__("%Hh%M")))
        return super().form_valid(form)
