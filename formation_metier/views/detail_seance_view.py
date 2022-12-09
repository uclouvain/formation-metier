from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View

from formation_metier.views.detail_seance_par_formateur_view import DetailSeanceParFormateur, \
    InscriptionParFormateurFormView
from formation_metier.views.detail_seance_par_participant_view import DetailSeanceForParticipant, \
    InscriptionParParticipantFormView


class DetailSeanceView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'formation_metier.access_to_formation_fare'
    name = 'detail_seance'

    def get(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='FormateurGroup').exists():
            view = DetailSeanceParFormateur.as_view()
        else:
            view = DetailSeanceForParticipant.as_view()
        return view(
            request,
            *args,
            **kwargs
        )

    def post(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='FormateurGroup').exists():
            view = InscriptionParFormateurFormView.as_view()
        else:
            view = InscriptionParParticipantFormView.as_view()
        return view(
            request,
            *args,
            **kwargs
        )
