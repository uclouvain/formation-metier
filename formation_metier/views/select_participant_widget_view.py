from dal import autocomplete
from django.utils.html import format_html

from formation_metier.models.person import Person


class PersonAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Person.objects.none()

        qs = Person.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

    def get_result_label(self, result):
        return format_html('<span>{}<span>', result.name)
