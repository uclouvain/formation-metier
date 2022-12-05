from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View

from formation_metier.views.detail_seance_for_formateur_view import DetailSeanceForFormateur, \
    RegisterForFormateurFormView
from formation_metier.views.detail_seance_for_participant_view import DetailSeanceForParticipant, \
    RegisterForParticipantFormView


class DetailSeanceView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'formation_metier.access_to_formation_fare'
    name = 'detail_seance'

    def get(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='FormateurGroup').exists():
            view = DetailSeanceForFormateur.as_view()
        else:
            view = DetailSeanceForParticipant.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='FormateurGroup').exists():
            view = RegisterForFormateurFormView.as_view()
        else:
            view = RegisterForParticipantFormView.as_view()
        return view(request, *args, **kwargs)
