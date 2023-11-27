# payment/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import stripe

from authentication.models import CustomUser
from product.models import CartItem
from .models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def proceed_to_checkout(request):
    try:
        # user = request.user
        user = CustomUser.objects.get(username='arham')
        print("User Authenticated:", request.user.is_authenticated)

        cart_items = CartItem.objects.filter(user=user)
        print(cart_items)

        if cart_items.exists():
            total_amount = sum(item.total_amount for item in cart_items)
            print("Total Amount:", total_amount)

            # Create a payment intent using the Stripe API
            stripe.api_key = 'sk_test_51OFGO7SJB5YS4H7OfA4yf3XoIh1vxPj5zmjq5xMTwny2pjsBRF95AFPVyHxKjtTt3DsPCy1JaK1mDNaCep7ohPbf00hul0RCdi'  # Replace with your actual secret key
            intent = stripe.PaymentIntent.create(
                amount=int(total_amount * 100),  # Amount in cents
                currency='usd',
                metadata={'cart_items': ', '.join([str(item.id) for item in cart_items])},
            )

            # Pass relevant data to the checkout template
            return render(request, 'checkout.html', {'client_secret': intent.client_secret, 'total_amount': total_amount})

        else:
            return render(request, 'empty_cart.html')

    except Exception as e:
        print("Exception:", str(e))
        # Handle the exception or log it for debugging
        return render(request, 'error_page.html', {'error_message': str(e)})

# Add a helper function to calculate the total amount
def calculate_total_amount(cart_items):
    # Add your logic to calculate the total amount based on cart items
    # For example, you can iterate through cart_items and sum the product prices.
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    return total_amount


@login_required
def stripe_payment(request):
    if request.method == 'POST':
        # Process the payment and update your database as needed
        # (e.g., mark the order as paid)

        # Example: Mark all cart items as paid
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        for cart_item in cart_items:
            # Perform actions needed to mark the order as paid
            cart_item.paid = True
            cart_item.save()

        # Clear the user's cart after successful payment
        CartItem.objects.filter(user=user).delete()

        # Return a JSON response indicating success
        return JsonResponse({'success': True})

    # Return a JSON response indicating failure
    return JsonResponse({'success': False}, status=400)