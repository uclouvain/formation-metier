from dal import autocomplete
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.utils.html import format_html

from formation_metier.models.participant import Participant


class PersonAutoComplete(LoginRequiredMixin, PermissionRequiredMixin, autocomplete.Select2QuerySetView):
    permission_required = 'formation_metier.view_participant'
    name = 'widget_participant'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Participant.objects.none()

        qs = Participant.objects.all()

        if self.q:
            qs = qs.filter(person__name__istartswith=self.q)

        return qs

    def get_result_label(self, result):
        return format_html('<span>{}<span>', result.person.name)
