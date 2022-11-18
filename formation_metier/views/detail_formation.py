from django.db.models import Count
from django.views import generic

from formation_metier.models.formation import Formation


class DetailFormation(generic.DetailView):
    model = Formation
    template_name = 'formation_metier/detail_formation.html'
    context_object_name = "formation"
    pk_url_kwarg = 'formation_id'
    name = 'detail_formation'

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['formation_id']).prefetch_related(
            'session_set',
            'session_set__register_set',
        )
