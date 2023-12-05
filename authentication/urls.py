from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('blog/', blog, name='blog'),
    path('contact_us/', ContactUs, name='contact_us'),
    path('signup/', SignUpPage, name='signup'),
    path('login/', LoginPage, name='login'),
    path('logout/', LogoutPage, name='logout'),
    path('profile_setup/', profile_setup, name='profile_setup'),
    path('request_product_form/', request_product_form, name='request_product_form'),
    path('delivery_Information/', deliveryInformation, name='delivery_Information'),
    path('payment_method/', PaymentMethod, name='payment_method'),
    path('privacy_policy/', PrivacyPolicy, name='privacy_policy'),
    path('term_conditions/', TermsAndConditions, name='term_conditions'),
    path('return_refunds/', ReturnAndRefunds, name='return_refunds'),
    path('success/', success_page, name='success_page'),
    path('About_us/', AboutUs, name='About_us'),
    path('faqs/', FAQS, name='faqs')

]
