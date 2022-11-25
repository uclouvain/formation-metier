from dal import autocomplete
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.utils.html import format_html

from formation_metier.models.person import Person


class PersonAutoComplete(LoginRequiredMixin, PermissionRequiredMixin, autocomplete.Select2QuerySetView):
    permission_required = ['formation_metier.view_participant', 'formation_metier.access_to_formation_fare']
    name = 'widget_participant'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Person.objects.none()

        qs = Person.objects.all()

        if self.q:
            qs = qs.filter(person__name__istartswith=self.q)

        return qs

    def get_result_label(self, result):
        return format_html('<span>{}<span>', result.person.name)
