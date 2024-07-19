from django import template
from accounts.models import User

register = template.Library()


@register.inclusion_tag("accounts/base_theme.html")
def base_theme_input():
    ...
    # users = User.objects.all()
    # return {'users':users}
