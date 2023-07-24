from django import template
from users.models import User

register = template.Library()

@register.filter
def get_date(date):    
    return "Y-M-d"