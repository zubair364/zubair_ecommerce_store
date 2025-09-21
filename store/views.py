from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem, Order, OrderItem


def _get_session_key(request):
    """
    Ensure the user has a session and return its key.
    """
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key


def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, "store/product_list.html", {"products": products})


def add_to_cart(request, product_id):
    session_key = _get_session_key(request)
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        session_key=session_key,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"Added {product.name} to your cart.")
    return redirect("product_list")


def view_cart(request):
    session_key = _get_session_key(request)
    cart_items = CartItem.objects.filter(session_key=session_key)
    total = sum(item.total_price() for item in cart_items)
    return render(request, "store/cart.html", {"cart_items": cart_items, "total": total})


def checkout(request):
    session_key = _get_session_key(request)
    cart_items = CartItem.objects.filter(session_key=session_key)

    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        if not cart_items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect("product_list")

        # Create the order
        order = Order.objects.create(
            name=name,
            address=address,
            phone=phone,
            payment_method="COD"
        )

        # Create order items and (optionally) reduce stock
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            # Optional: reduce stock
            if item.product.stock is not None:
                item.product.stock = max(0, item.product.stock - item.quantity)
                item.product.save()

        # Clear the cart for this session
        cart_items.delete()

        messages.success(request, "Your order has been placed successfully! (Cash on Delivery)")
        return redirect("product_list")

    # GET: render checkout form
    return render(request, "store/checkout.html")

def about_us(request):
    return render(request, "store/about.html")

def services(request):
    return render(request, "store/services.html")
