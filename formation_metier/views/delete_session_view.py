from typing import Union
from django.contrib import messages
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect
from formation_metier.models.session import Session


def delete_session(request, session_id: str) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
    session = Session.objects.get(id=session_id)
    session.delete()
    messages.success(request, 'La session du {} à {} a été supprimée.'.format(session.date_format(),
                                                                              session.time_format()))
    return redirect('formation_metier:detail_formation', session.formation.id)
