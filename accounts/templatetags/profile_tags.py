from django import template
from accounts.models import blood_group_choices,marital_status_choices

register = template.Library()

@register.filter
def full_blood_group(q):
    for choice in blood_group_choices:
        if choice[0] == q:
            return choice[1]
    return ''

@register.filter
def full_marital_status(q):
    for choice in marital_status_choices:
        if choice[0] == q:
            return choice[1]
    return ''

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
