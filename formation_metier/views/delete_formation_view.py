from typing import Union
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect
from django.views import generic

from formation_metier.models.formation import Formation


@login_required
@permission_required('formation_metier.delete_formation', raise_exception=True)
@permission_required('formation_metier.access_to_formation_fare', raise_exception=True)
def delete_formation(request, formation_id) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
    formation = Formation.objects.get(id=formation_id)
    formation.delete()
    messages.success(request, 'La formation {} a été supprimée.'.format(formation.name))
    return redirect('formation_metier:list_formation')


class DeleteFormation(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    permission_required = 'formation_metier.delete_formation'
    model = Formation
    # success_url = '/list_formation'

    pk_url_kwarg = "formation_id"

    def get_success_url(self):
        success_message = f'La formation {self.object.name} a été supprimée.'
        messages.success(self.request, success_message)
        return '/list_formation'
