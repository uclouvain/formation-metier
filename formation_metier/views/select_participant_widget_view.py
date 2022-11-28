from dal import autocomplete
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.utils.html import format_html

from formation_metier.models.employe_uclouvain import EmployeUCLouvain


class PersonAutoComplete(LoginRequiredMixin, PermissionRequiredMixin, autocomplete.Select2QuerySetView):
    permission_required = ['formation_metier.view_participant', 'formation_metier.access_to_formation_fare']
    name = 'widget_participant'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return EmployeUCLouvain.objects.none()

        qs = EmployeUCLouvain.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

    def get_result_label(self, result):
        return format_html('<span>{}<span>', result.name)
