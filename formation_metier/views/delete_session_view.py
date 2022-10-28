from django.shortcuts import redirect
from formation_metier.models.session import Session


def delete_session(request, session_id):
    session = Session.objects.get(id=session_id)
    session.delete()
    return redirect('formation_metier:detail_formation', session.formation.id)
