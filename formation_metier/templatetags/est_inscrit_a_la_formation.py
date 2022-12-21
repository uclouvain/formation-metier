from django import template

register = template.Library()


@register.filter(name='est_inscrit_formation')
def est_inscrit_formation(user, formation):
    for seance in formation.seance_set.all():
        for inscription_object in seance.inscription_set.all():
            if user.employeuclouvain == inscription_object.participant:
                return True
    return False
