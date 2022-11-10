from django.db import models


class RoleOsis(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
