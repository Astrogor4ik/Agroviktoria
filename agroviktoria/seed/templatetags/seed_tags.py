from django import template
from ..models import *

register = template.Library()


@register.simple_tag()
def prod_discount():
    res = Category.objects.all()
    #prise_d = price + 5
    #price_d = price + 5
    return res
