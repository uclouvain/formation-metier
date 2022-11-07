from formation_metier.models.session import Session
from django import template

register = template.Library()


@register.simple_tag
def public_cible_display(session: Session):
    return session.get_public_cible_display()
