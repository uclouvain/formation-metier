from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect

from formation_metier.models.register import Register
from django.views.generic import DeleteView


class DeleteRegister(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = ['formation_metier.delete_register', 'formation_metier.access_to_formation_fare']
    model = Register
    pk_url_kwarg = "seance_id"

    def get_queryset(self):
        register_list = self.request.POST.getlist('inscription')
        return Register.objects.filter(id__in=register_list, seance_id=self.request.POST.get("seance_id"))

    def delete(self, request, *args, **kwargs):
        if request.method == "POST":
            register_list = self.get_queryset()
            seance_id = request.POST.get("seance_id")
            for register_object in register_list:
                messages.success(request, "L'inscription de l'utilisateur '{}' a été supprimée.".format(
                    register_object.participant.name))
            register_list.delete()
            return redirect('formation_metier:detail_seance', seance_id)
