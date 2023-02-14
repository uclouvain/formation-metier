from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Prefetch
from django.views import generic

from formation_metier.models.formation import Formation
from formation_metier.models.seance import Seance


class DetailFormation(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    permission_required = [
        'formation_metier.view_formation',
        'formation_metier.view_seance',
        'formation_metier.access_to_formation_fare'
    ]
    model = Formation
    template_name = 'formation_metier/detail_formation.html'
    context_object_name = "formation"
    pk_url_kwarg = 'formation_id'
    name = 'detail_formation'

    def get_queryset(self):
        return super().get_queryset().filter(
            id=self.kwargs['formation_id']
        ).order_by(
            'name'
        ).prefetch_related(
            Prefetch(
                'seance_set',
                queryset=Seance.objects.order_by('seance_date')
            ),
            'seance_set__inscription_set',
            'seance_set__formateur',
        )