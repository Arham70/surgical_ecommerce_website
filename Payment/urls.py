# payment/urls.py
# Update this line in your imports
from django.contrib import admin
# urls.py
from django.urls import path
from .views import CheckoutPageView, charge, order_list

urlpatterns = [
    path('checkout/', CheckoutPageView.as_view(), name='checkout'),
    path('charge/', charge, name='charge'),
    path('order_list/', order_list, name='order_list'),
]

