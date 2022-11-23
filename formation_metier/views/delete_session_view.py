from typing import Union
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect
from formation_metier.models.session import Session


@login_required
@permission_required('formation_metier.delete_session', raise_exception=True)
@permission_required('formation_metier.access_to_formation_fare', raise_exception=True)
def delete_session(request, session_id: str) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
    session = Session.objects.get(id=session_id)
    session.delete()
    messages.success(request, 'La session du {} à {} a été supprimée.'.format(session.date_format(),
                                                                              session.time_format()))
    return redirect('formation_metier:detail_formation', session.formation.id)
