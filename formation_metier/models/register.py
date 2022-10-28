import django.utils.timezone
from django.db import models
from datetime import datetime

from formation_metier.models import session


class Register(models.Model):
    session = models.ForeignKey(session.Session, on_delete=models.CASCADE)
    participant = models.CharField(max_length=50)
    register_date = models.DateTimeField(auto_now_add=True)
