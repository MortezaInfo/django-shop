from django import template
from accounts.models import User
from ..forms import FilterProductForm


register = template.Library()


@register.inclusion_tag("home/base_filter.html")
def filter_product():
    return {
        'form_filter':FilterProductForm
    }