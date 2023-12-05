import stripe
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.conf import settings

from django.views.generic.base import TemplateView
from pyexpat.errors import messages

from Payment.models import Payment, Order
from product.models import CartItem


class CheckoutPageView(TemplateView):
    template_name = 'checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate the total amount from cart_items in cents
        cart_items = CartItem.objects.filter(user=self.request.user)
        total_amount_dollars = sum(item.product.price * item.quantity for item in cart_items)


        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        context['total_amount'] = total_amount_dollars
        return context


@transaction.atomic
def charge(request):
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Get the user's cart items
        cart_items = CartItem.objects.filter(user=request.user)

        # Calculate the total amount in dollars
        total_amount_dollars = sum(item.product.price * item.quantity for item in cart_items)

        try:
            # Create a Stripe charge
            charge = stripe.Charge.create(
                amount=int(total_amount_dollars * 100),  # Convert to cents
                currency='usd',
                description='Payment Gateway',
                source=request.POST['stripeToken']
            )

            with transaction.atomic():
                orders = []
                for cart_item in cart_items:
                    order = Order.objects.create(
                        user=request.user,
                        product_name=cart_item.product.name,
                        price=cart_item.product.price,
                        quantity=cart_item.quantity,
                        subtotal=cart_item.product.price * cart_item.quantity,
                        paid=True
                    )
                    orders.append(order)
            # If the charge is successful, create a Payment record and delete the cart items
            with transaction.atomic():
                payment = Payment.objects.create(
                    user=request.user,
                    product=cart_items.first().product,  # Use the product from the first cart item for simplicity
                    amount=total_amount_dollars,
                    is_paid=True
                )

                # Delete the cart items
                cart_items.delete()

            # Redirect to a success page or render the charge.html page
            return render(request, 'charge.html', {'payment': payment})
        except stripe.error.StripeError as e:
            # Handle Stripe errors
            messages.error(request, f"Error processing payment: {str(e)}")
            return redirect('checkout')


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_list.html', {'orders': orders})
