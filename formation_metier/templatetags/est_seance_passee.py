import datetime

from django import template

register = template.Library()


@register.filter(name='est_seance_passee')
def est_seance_passe(seance):
    date_actuelle = datetime.datetime.now()
    if seance.seance_date < date_actuelle:
        return True
    else:
        return False
