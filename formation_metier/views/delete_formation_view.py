from typing import Union
from django.contrib import messages
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect
from formation_metier.models.formation import Formation


def delete_formation(request, formation_id) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
    formation = Formation.objects.get(id=formation_id)
    formation.delete()
    messages.success(request, 'La formation {} a été supprimée.'.format(formation.name))
    return redirect('formation_metier:list_formation')
