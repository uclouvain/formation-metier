from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic

from formation_metier.models.session import Session


class UpdateSessionView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Session
    fields = ['session_date', 'local', 'participant_max_number', 'formateur_id', 'public_cible']
    template_name = 'formation_metier/update_session.html'
    pk_url_kwarg = "session_id"

    def get_success_url(self):
        return reverse('formation_metier:detail_session', kwargs={'session_id': self.kwargs['session_id']})
