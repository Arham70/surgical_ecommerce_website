from django.contrib import admin
from .models import CartItem, Product, Size, Review

admin.site.register(Product)
admin.site.register(Size)
admin.site.register(CartItem)


@admin.register(Review)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'created_at', 'modified_at', 'comment', 'rating']