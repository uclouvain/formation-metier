from dal import autocomplete
from django.utils.html import format_html

from formation_metier.models.participant import Participant


class PersonAutoComplete(autocomplete.Select2QuerySetView):
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
