from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views import generic

from formation_metier.models.session import Session


class UpdateSessionView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.edit.UpdateView):
    permission_required = ['formation_metier.change_session', 'formation_metier.access_to_formation_fare']
    model = Session
    fields = ['session_date', 'local', 'participant_max_number', 'formateur', 'duree']
    template_name = 'formation_metier/update_session.html'
    pk_url_kwarg = "session_id"
    success_message = 'La session a été modifiée.'
    name = 'update_session'

    def get_success_url(self):
        return reverse('formation_metier:detail_session', kwargs={'session_id': self.kwargs['session_id']})
