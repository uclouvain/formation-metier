from django.shortcuts import render
from formation_metier.models.formation import Formation


def delete_formation(request, formation_id):
    formation = Formation.objects.get(id=formation_id)
    formation.delete()
    return render(request, 'formation_metier/index.html')
