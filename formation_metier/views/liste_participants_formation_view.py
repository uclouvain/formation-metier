from django.views import generic

from formation_metier.models.employe_uclouvain import EmployeUCLouvain
from formation_metier.models.formation import Formation


class ListeParticipantsFormationView(generic.ListView):
    model = EmployeUCLouvain
    name = "liste_participants_formations"
    context_object_name = "liste_participants"
    template_name = "formation_metier/liste_participants_formation.html"
    pk_url_kwarg = "formation_id"

    def get_queryset(self):
        return super().get_queryset().filter(
            inscription__seance__formation_id=self.kwargs["formation_id"]).distinct().order_by('name')

    def get_context_data(self, *, object_list=None, **kwargs):
        return {**super().get_context_data(object_list=object_list, **kwargs),
                'formation': Formation.objects.get(id=self.kwargs["formation_id"])
                }
