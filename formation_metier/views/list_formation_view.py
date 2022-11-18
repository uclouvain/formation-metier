from django.views import generic

from formation_metier.models.formation import Formation


class ListFormationView(generic.ListView):
    model = Formation
    template_name = "formation_metier/list_formation.html"
    context_object_name = 'formation_list'
    name = 'list_formation'

    def get_queryset(self):
        queryset = Formation.objects.all()
        return queryset
