from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic

from formation_metier.models.formation import Formation


class ListeFormationView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = [
        'formation_metier.view_formation',
        'formation_metier.access_to_formation_fare'
    ]
    model = Formation
    template_name = "formation_metier/liste_des_formation.html"
    context_object_name = 'formation_liste'
    name = 'liste_formation'
    queryset = Formation.objects.all().order_by('name')
