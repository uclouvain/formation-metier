from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic

from formation_metier.models.formation import Formation


class ListFormationView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = ['formation_metier.view_formation', 'formation_metier.access_to_formation_fare']
    model = Formation
    template_name = "formation_metier/list_formation.html"
    context_object_name = 'formation_list'
    name = 'list_formation'

    def get_queryset(self):
        queryset = Formation.objects.all()
        return queryset
