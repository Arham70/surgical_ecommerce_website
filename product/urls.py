from django.urls import path
from .views import featured_products, product_detail, add_to_cart, view_cart, remove_from_cart, empty_cart_view, get_cart_count, create_review

urlpatterns = [
    path('featured_products/', featured_products, name='featured_products'),
    path('product_detail/<int:product_id>/', product_detail, name='product_detail'),
    path('create-review/<int:prod_id>/', create_review, name='create-review'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('view_cart/', view_cart, name='view_cart'),
    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('empty-cart/', empty_cart_view, name='name_of_empty_cart_view'),
    path('get_cart_count/', get_cart_count, name='get_cart_count'),
]