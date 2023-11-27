# payment/urls.py
from django.urls import path
from .views import proceed_to_checkout, stripe_payment

urlpatterns = [
    path('proceed-to-checkout/', proceed_to_checkout, name='proceed_to_checkout'),
    path('stripe-payment/', stripe_payment, name='stripe_payment'),
]
