from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DeleteView
from formation_metier.models.session import Session


def delete_session(request, session_id):
    # remove the contact from list.
    session = Session.objects.get(id=session_id)
    session.delete()
    return redirect('formation_metier:detail_formation', session.formation.id)
