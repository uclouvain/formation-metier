from typing import Union
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect
from formation_metier.models.seance import Seance


@login_required
@permission_required('formation_metier.delete_seance', raise_exception=True)
@permission_required('formation_metier.access_to_formation_fare', raise_exception=True)
def delete_seance(request, seance_id: str) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
    seance = Seance.objects.get(id=seance_id)
    seance.delete()
    messages.success(request,
                     'La seance du {} à {} a été supprimée.'.format(seance.seance_date.__format__("%d/%m/%Y"),
                                                                    seance.time_format()))
    return redirect('formation_metier:detail_formation', seance.formation.id)
