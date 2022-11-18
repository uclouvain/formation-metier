from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from formation_metier.models.register import Register


def delete_registration(request, register_id) -> HttpResponseRedirect:
    registration = Register.objects.get(id=register_id)
    url = reverse('formation_metier:detail_session', kwargs={'session_id': registration.session_id})
    registration.delete()
    messages.success(request, "L'inscription de l'utilisateur {} a été supprimée.".format(
        registration.participant.name))
    return HttpResponseRedirect(url)
