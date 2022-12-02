from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.edit import FormView

from formation_metier.forms.new_register_for_current_user import NewRegisterForCurrentUser
from formation_metier.models.employe_uclouvain import EmployeUCLouvain
from formation_metier.models.register import Register
from formation_metier.models.seance import Seance


@login_required
@permission_required('formation_metier.add_register', raise_exception=True)
@permission_required('formation_metier.access_to_formation_fare', raise_exception=True)
def add_self_registration(request, seance_id: str) -> HttpResponseRedirect:
    if request.method == 'POST':
        seance = get_object_or_404(Seance, id=seance_id)
        user = request.user
        employe_ucl = get_object_or_404(EmployeUCLouvain, user=user)
        register_object = Register(participant=employe_ucl, seance=seance)
        register_set = seance.register_set.all()
        for register in register_set:
            if register.participant == employe_ucl:
                raise IntegrityError("Vous ếtes déjà inscrit à cette séance")
        if seance.participant_max_number <= register_set.count():
            raise ValidationError("Le nombre maximal de participant inscit à cette seance est déjà atteint")
        register_object.save()
        messages.success(request, f"Votre inscription à la séance ' {seance} ' a été ajouté.")
        return redirect('formation_metier:detail_seance', seance_id)

class RegisterCurrentUser(FormView):
    model = Register
    form_class = NewRegisterForCurrentUser



