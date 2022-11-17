from django.contrib import messages
from django.shortcuts import render
from formation_metier.models.formation import Formation


def delete_formation(request, formation_id):
    formation = Formation.objects.get(id=formation_id)
    formation.delete()
    messages.success(request, 'La formation {} a été supprimée.'.format(formation.name))
    return render(request, 'formation_metier/list_formation.html')
