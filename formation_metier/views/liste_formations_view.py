from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef
from django.views import generic

from formation_metier.models.formation import Formation
from formation_metier.models.inscription import Inscription


class ListeFormationView(LoginRequiredMixin, generic.ListView):
    model = Formation
    template_name = "formation_metier/liste_formations.html"
    context_object_name = 'liste_formations'
    name = 'liste_formations'

    def get_queryset(self):
        return super().get_queryset().order_by('name').annotate(
            est_inscrit_formation=Exists(
                Inscription.objects.filter(
                    participant=self.request.user.employeuclouvain,
                    seance__formation=OuterRef('pk')
                )
            ),
            est_user_formateur=Exists(
                self.request.user.groups.filter(name='FormateurGroup')
            )
        )
