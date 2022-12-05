from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.views.generic import DeleteView

from formation_metier.models.register import Register
from formation_metier.models.seance import Seance


class DeleteSelfRegister(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = ['formation_metier.delete_self_register', 'formation_metier.access_to_formation_fare']
    model = Register
    name = 'delete_self_registration'

    def get_queryset(self):
        self.request.POST.get('seance_id')
        register = Register.objects.get(participant=self.request.user.employeuclouvain,
                                           seance_id=self.request.POST.get("seance_id"))
        return register

    def delete(self, request, *args, **kwargs):
        if request.method == "POST":
            register = self.get_queryset()
            if register is None:
                raise AssertionError("Vous n'êtes pas inscrit à cette seance")
            else:
                seance_id = request.POST.get("seance_id")
                messages.success(request,
                                 f"Votre inscription à la seance du {register.seance.seance_date.date()} pour la formation '{register.seance.formation}'  a été supprimée.")
                register.delete()
            return redirect('formation_metier:detail_seance', seance_id)
