from dal import autocomplete
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.utils.html import format_html

from formation_metier.models.employe_uclouvain import EmployeUCLouvain
from formation_metier.models.inscription import Inscription


class SelectionParticipantAutoComplete(LoginRequiredMixin, PermissionRequiredMixin, autocomplete.Select2QuerySetView):
    permission_required = [
        'formation_metier.view_employeuclouvain',
        'formation_metier.access_to_formation_fare'
    ]
    name = 'widget_participant'

    def get_queryset(self):
        seance = self.forwarded['seance']
        inscription_list = [x.participant.name for x in Inscription.objects.filter(seance__id=seance)]
        qs = EmployeUCLouvain.objects.exclude(name__in=inscription_list)
        if self.q:
            qs = qs.filter(name__icontains=self.q).order_by('name')
        return qs

    def get_result_label(self, result):
        return format_html('<span>{}<span>', result.name)
