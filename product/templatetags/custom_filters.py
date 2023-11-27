# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()


@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg


@register.filter
def multiply_total(cart_items):
    total = sum(item.product.price * item.quantity for item in cart_items)
    return f'{total:.2f}'