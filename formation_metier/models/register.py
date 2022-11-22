import django.utils.timezone
from django.db import models
from datetime import datetime

from django.db.models import UniqueConstraint

from formation_metier.models import session, participant


class Register(models.Model):
    session = models.ForeignKey(session.Session, on_delete=models.CASCADE, blank=False)
    participant = models.ForeignKey(participant.Participant, on_delete=models.CASCADE, blank=False)
    register_date = models.DateTimeField(auto_now_add=True, blank=False)

    class Meta:
        constraints = [UniqueConstraint(fields=['session', 'participant'], name='unique_register')]
