from django import template

register = template.Library()


@register.filter(name='est_membre_du_groupe')
def est_membre_du_groupe(user, nom_du_groupe):
    return user.groups.filter(name=nom_du_groupe).exists()
