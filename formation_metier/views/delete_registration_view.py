from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from formation_metier.models.register import Register


def delete_registration(request) -> HttpResponseRedirect:
    if request.method == "POST":
        register_list = request.POST.getlist('inscription')
        register_object_list = []
        session_id = ""
        for register in register_list:
            register_object = get_object_or_404(Register, pk=register)
            register_object_list.append(register_object)
            if session_id == "":
                session_id = register_object.session.id
        for register_object in register_object_list:
            register_object.delete()
            messages.success(request, "L'inscription de l'utilisateur '{}' a été supprimée.".format(
                register_object.participant.name))
        return redirect('formation_metier:detail_session', session_id)
