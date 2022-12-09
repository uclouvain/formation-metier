from django import template

register = template.Library()


@register.filter(name='est_inscrit_seance')
def est_inscrit_seance(user, seance):
    for inscription_object in seance.inscription_set.all():
        if user.employeuclouvain == inscription_object.participant:
            return True
    return False
