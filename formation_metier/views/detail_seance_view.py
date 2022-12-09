from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django.views import View, generic
from django.views.generic.edit import FormMixin

from formation_metier.forms.nouvelle_inscription_par_formateur_form import NouvelleInscriptionParFormateurForm
from formation_metier.forms.nouvelle_inscription_par_participant_form import NouvelleInscriptionParParticipantForm
from formation_metier.models.seance import Seance
from formation_metier.views.detail_seance_par_formateur_view import InscriptionParFormateurFormView
from formation_metier.views.detail_seance_par_participant_view import InscriptionParParticipantFormView


class DetailSeance(LoginRequiredMixin, PermissionRequiredMixin, FormMixin, generic.DetailView):
    permission_required = [
        'formation_metier.view_seance',
        'formation_metier.view_inscription'
    ]
    model = Seance
    template_name = 'formation_metier/detail_seance.html'
    context_object_name = "seance"
    pk_url_kwarg = 'seance_id'

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'form': self.get_form()
        }

    def get_form_kwargs(self):
        return {
            **super().get_form_kwargs(),
            'seance': self.get_object()
        }

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['seance_id']).prefetch_related(
            'inscription_set',
            'inscription_set__participant'
        ).annotate(
            inscription_count=Count('inscription'),
        )

    def get_form_class(self):
        if self.request.user.groups.filter(name='FormateurGroup').exists():
            return NouvelleInscriptionParFormateurForm
        elif self.request.user.groups.filter(name='ParticipantGroup').exists():
            return NouvelleInscriptionParParticipantForm


class DetailSeanceView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'formation_metier.access_to_formation_fare'
    name = 'detail_seance'

    def get(self, request, *args, **kwargs):
        view = DetailSeance.as_view()
        return view(
            request,
            *args,
            **kwargs
        )

    def post(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='FormateurGroup').exists():
            view = InscriptionParFormateurFormView.as_view()
        else:
            view = InscriptionParParticipantFormView.as_view()
        return view(
            request,
            *args,
            **kwargs
        )
