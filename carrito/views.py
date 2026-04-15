from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .cart import Cart
from .models import Order, OrderItem
from productos.models import Product
from core.models import StoreConfig


def add_product(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    messages.success(request, f'add|{product.name}')
    return redirect(request.META.get("HTTP_REFERER", "catalog"))


def remove_one(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove_one(product)
    messages.info(request, f'sub|{product.name}')
    return redirect("cart")


def remove_product(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    name = product.name
    cart.remove(product)
    messages.warning(request, f'del|{name}')
    return redirect("cart")


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    messages.warning(request, 'clear|')
    return redirect("cart")


def view_cart(request):
    cart = Cart(request)
    store = StoreConfig.get()
    return render(request, "carrito/Cart.html", {
        "cart": cart,
        "total": cart.total(),
        "store_open": store.is_open,
        "closed_message": store.closed_message,
    })


@login_required
def checkout(request):
    if request.method == "POST":

        store = StoreConfig.get()
        if not store.is_open:
            cart = Cart(request)
            return render(request, "carrito/Cart.html", {
                "cart": cart,
                "total": cart.total(),
                "store_open": False,
                "closed_message": store.closed_message,
                "checkout_error": store.closed_message,
            })

        cart = Cart(request)

        if not cart.cart:
            return redirect("cart")

        order = Order.objects.create(
            user=request.user,
            total=cart.total(),
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product_id=item["product_id"],
                name=item["name"],
                price=item["price"],
                quantity=item["quantity"],
                image=item.get("image", ""),
            )

        cart.clear()
        messages.success(request, f'order|{order.id}')
        return redirect("order_confirmation", order_id=order.id)

    return redirect("cart")


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "carrito/Confirmation.html", {"order": order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "carrito/Orders.html", {"orders": orders})
