from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views import generic

from formation_metier.models.employe_uclouvain import EmployeUCLouvain, RoleFormationFareEnum
from formation_metier.models.seance import Seance


class ModificationSeanceView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.edit.UpdateView):
    permission_required = ['formation_metier.change_seance', 'formation_metier.access_to_formation_fare']
    model = Seance
    fields = ['seance_date', 'local', 'participant_max_number', 'formateur', 'duree']
    template_name = 'formation_metier/modification_seance_form.html'
    pk_url_kwarg = "seance_id"
    success_message = 'La seance a été modifiée.'
    name = 'modification_seance'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['formateur'].queryset = EmployeUCLouvain.objects.filter(
            role_formation_metier=RoleFormationFareEnum.FORMATEUR)
        return form

    def get_success_url(self):
        return reverse('formation_metier:detail_seance', kwargs={'seance_id': self.kwargs['seance_id']})
