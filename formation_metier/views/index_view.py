from django.views import generic

from formation_metier.models.formation import Formation


class IndexView(generic.ListView):
    model = Formation
    template_name = "formation_metier/index.html"
    context_object_name = 'formation_list'

    def get_queryset(self):
        queryset = Formation.objects.all()
        return queryset
