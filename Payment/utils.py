# payment/utils.py
from .models import Payment

def create_order(user, product, amount):
    # Create a payment order
    payment_order = Payment.objects.create(
        user=user,
        product=product,
        amount=amount,
        is_paid=True  # Assuming the order is considered paid upon creation
    )

    return payment_order
