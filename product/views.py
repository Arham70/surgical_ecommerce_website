from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, CartItem


def featured_products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    sizes = product.sizes.all()
    return render(request, 'SingleProduct.html', {'product': product, 'sizes': sizes})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        # If the item already exists in the cart, increase the quantity
        cart_item.quantity += 1
    cart_item.total_amount = cart_item.quantity * product.price  # Calculate and set total amount
    cart_item.save()

    return JsonResponse({'success': True})



def view_cart(request):
    cart_items = CartItem.objects.all()
    return render(request, 'cart.html', {'cart_items': cart_items})


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')

def empty_cart_view(request):
    return render(request, 'empty_cart.html')