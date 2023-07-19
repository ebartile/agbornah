from django import template
from users.models import User

register = template.Library()

@register.filter
def get_email(id):
    user = User.objects.get(id=id)
    return user.email
