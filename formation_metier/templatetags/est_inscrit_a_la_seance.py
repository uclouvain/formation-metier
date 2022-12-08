from django import template

register = template.Library()


@register.filter(name='est_inscrit')
def est_inscrit(user, seance):
    for inscription_object in seance.inscription_set.all():
        if user.employeuclouvain == inscription_object.participant:
            return True
    return False

