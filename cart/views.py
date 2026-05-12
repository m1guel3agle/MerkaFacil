from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .cart import Cart
from .models import Order, OrderItem
from products.models import Product
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
    return render(request, "cart/Cart.html", {
        "cart": cart,
        "total": cart.total(),
        "store_open": store.is_open,
        "closed_message": store.closed_message,
    })


@login_required
def checkout(request):
    """Primera etapa: crear la orden y redirigir a selección de entrega"""
    if request.method == "POST":

        store = StoreConfig.get()
        if not store.is_open:
            cart = Cart(request)
            return render(request, "cart/Cart.html", {
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
        return redirect("select_delivery", order_id=order.id)

    return redirect("cart")


@login_required
# FR-4: Seleccionar método de entrega
def select_delivery(request, order_id):
    """Seleccionar método de entrega: delivery o pickup"""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == "POST":
        delivery_method = request.POST.get("delivery_method")

        if delivery_method not in ["pickup", "delivery"]:
            return redirect("select_delivery", order_id=order.id)

        order.delivery_method = delivery_method

        # Si es delivery, agregar costo de envío (5.000 pesos)
        if delivery_method == "delivery":
            order.total += 5000

        order.save()

        if delivery_method == "delivery":
            return redirect("select_payment", order_id=order.id)
        else:
            return redirect("order_confirmation", order_id=order.id)

    return render(request, "cart/SelectDelivery.html", {"order": order})


# FR-5: Seleccionar método de pago
@login_required
def select_payment(request, order_id):
    """Seleccionar método de pago: efectivo o tarjeta (solo para delivery)"""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Validar que sea delivery
    if order.delivery_method != "delivery":
        return redirect("order_confirmation", order_id=order.id)

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")

        if payment_method not in ["cash", "card"]:
            return redirect("select_payment", order_id=order.id)

        order.payment_method = payment_method
        order.save()

        return redirect("order_confirmation", order_id=order.id)

    return render(request, "cart/SelectPayment.html", {"order": order})


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "cart/Confirmation.html", {"order": order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "cart/Orders.html", {"orders": orders})


@login_required
def cancel_order(request, order_id):
    """Cancel an order only if it is within the 2-minute cancellation window."""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status != "pending":
        return JsonResponse(
            {"error": "Solo se pueden cancelar órdenes en estado pendiente."},
            status=400,
        )

    if timezone.now() > order.date + timedelta(minutes=2):
        return JsonResponse(
            {"error": "El tiempo límite de cancelación (2 minutos) ha expirado."},
            status=400,
        )

    order.status = "cancelled"
    order.save()

    return JsonResponse({
        "success": True,
        "message": f"Pedido #{order.id} cancelado correctamente.",
    })
