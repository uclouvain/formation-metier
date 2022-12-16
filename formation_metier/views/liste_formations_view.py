from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic

from formation_metier.models.formation import Formation


class ListeFormationView(LoginRequiredMixin, generic.ListView):
    model = Formation
    template_name = "formation_metier/liste_formations.html"
    context_object_name = 'liste_formations'
    name = 'liste_formations'
    queryset = Formation.objects.all().order_by('name')
