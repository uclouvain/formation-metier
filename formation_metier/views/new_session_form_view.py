from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from formation_metier.models.formation import Formation
from formation_metier.models.session import Session
from formation_metier.forms.new_session_form import NewSessionForm


class NewSessionFormView(generic.CreateView):
    model = Session
    template_name = 'formation_metier/new_session_form.html'
    form_class = NewSessionForm
    pk_url_kwarg = "formation_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formation_id"] = self.kwargs['formation_id']
        return context

    def get_success_url(self):
        return reverse('formation_metier:detail_formation', kwargs={'formation_id': self.kwargs['formation_id']})

    def form_valid(self, form):
        formation = get_object_or_404(Formation, id=self.kwargs['formation_id'])
        form.instance.formation = formation
        return super().form_valid(form)
