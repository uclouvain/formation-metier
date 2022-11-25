from formation_metier.models.formation import Formation
from django import template

register = template.Library()


@register.simple_tag
def public_cible_display(formation: Formation):
    return formation.get_public_cible_display()
