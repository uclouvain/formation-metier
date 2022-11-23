from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from formation_metier.models.register import Register
from formation_metier.models.session import Session


@login_required
@permission_required('formation_metier.delete_register', raise_exception=True)
@permission_required('formation_metier.access_to_formation_fare', raise_exception=True)
def delete_registration(request) -> HttpResponseRedirect:
    if request.method == "POST":
        register_list = request.POST.getlist('inscription')
        register_object_list = []
        session_id = request.POST.get("session_id")
        session_register_set = Session.objects.get(id=session_id).register_set.all()
        for register in register_list:
            register_object = get_object_or_404(Register, pk=register)
            if register_object not in session_register_set:
                raise ValueError("l'inscription n'appartient pas a la session actuelle")
            else:
                register_object_list.append(register_object)
        for register_object in register_object_list:
            register_object.delete()
            messages.success(request, "L'inscription de l'utilisateur '{}' a été supprimée.".format(
                register_object.participant.person.name))
        return redirect('formation_metier:detail_session', session_id)
