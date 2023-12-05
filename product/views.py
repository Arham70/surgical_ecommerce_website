from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, CartItem, Size
from .utils import recalculate_subtotal  # Assuming you've created a utils.py file

def featured_products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    sizes = Size.objects.all()
    return render(request, 'SingleProduct.html', {'product': product, 'sizes': sizes})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    quantity = int(request.GET.get('quantity', 1))  # Get the quantity from the request, default to 1 if not provided

    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)

    if not created:
        # If the item already exists in the cart, update the quantity
        cart_item.quantity += quantity
    else:
        # If the item is newly added, set the quantity
        cart_item.quantity = quantity

    # Calculate and set the total_amount when a new item is added or quantity is increased
    cart_item.total_amount = cart_item.product.price * cart_item.quantity

    cart_item.save()

    return JsonResponse({'success': True})


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
