from django.http import HttpResponseRedirect
from django.urls import reverse

from formation_metier.models.register import Register


def delete_registration(request, register_id):
    registration = Register.objects.get(id=register_id)
    url = reverse('formation_metier:detail_session', kwargs={'session_id': registration.session_id})
    registration.delete()
    return HttpResponseRedirect(url)
