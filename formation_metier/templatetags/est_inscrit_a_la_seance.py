from django import template

register = template.Library()


@register.filter(name='is_register')
def is_register(user, seance):
    for register_object in seance.register_set.all():
        if user.employeuclouvain == register_object.participant:
            return True
    return False
