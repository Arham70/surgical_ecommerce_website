from django.contrib import admin
from .models import CartItem, Product, Size

admin.site.register(Product)
admin.site.register(Size)
admin.site.register(CartItem)