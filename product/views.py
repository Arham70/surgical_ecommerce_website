from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import product
from .form import ReviewForm
from .models import Product, CartItem, Size, Review
from .utils import recalculate_subtotal  # Assuming you've created a utils.py file

def featured_products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    sizes = Size.objects.all()
    reviews = Review.objects.all()

    stars_range = range(1, 6)

    return render(request, 'SingleProduct.html', {'product': product, 'sizes': sizes, 'reviews': reviews, 'stars_range': stars_range})


def create_review(request, prod_id):
    product = get_object_or_404(Product, id=prod_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return render(request, 'SingleProduct.html')   # Redirect to a success page or product detail page

    return render(request, 'SingleProduct.html', {'form': ReviewForm()})


@csrf_exempt
@login_required
def add_to_cart(request):
    if request.method == 'POST' and request.user.is_authenticated:
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity', 1)

        product = get_object_or_404(Product, id=product_id)

        # Check if the product is already in the cart
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product
        )

        # If the cart item already exists, increment the quantity by 1
        if not created:
            cart_item.quantity += 1
        else:
            # If the cart item is newly created, set the quantity to the provided value
            cart_item.quantity = quantity

        # Save the cart item after updating the quantity
        cart_item.save()

        # Recalculate subtotal in utils.py (you need to implement this)
        recalculate_subtotal(request.user)

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)

    # Delete the cart item
    cart_item.delete()

    # Recalculate subtotal
    recalculate_subtotal(request.user)

    # Return a success response
    return JsonResponse({'success': True})


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_amount': total_amount})


def empty_cart_view(request):
    return render(request, 'empty_cart.html')


@login_required
def get_cart_count(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_cart_items = sum(item.quantity for item in cart_items)

    # Render the template with the cart count
    return render(request, 'SingleProduct.html', {'total_cart_items': total_cart_items})
