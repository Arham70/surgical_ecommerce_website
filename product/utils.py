from django import template
from .models import CartItem

register = template.Library()


@register.filter
def calculate_subtotal(cart_item):
    return cart_item.product.price * cart_item.quantity


def recalculate_subtotal(user):
    cart_items = CartItem.objects.filter(user=user)
    subtotal = sum(calculate_subtotal(item) for item in cart_items)