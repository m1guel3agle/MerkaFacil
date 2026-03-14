from django.shortcuts import redirect, render, get_object_or_404
from .carrito import Carrito
from productos.models import Producto


def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.agregar(producto)
    return redirect(request.META.get("HTTP_REFERER", "catalogo"))


def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.restar(producto)
    return redirect("carrito")


def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.eliminar(producto)
    return redirect("carrito")


def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("carrito")


def ver_carrito(request):
    carrito = Carrito(request)
    return render(request, "carrito/carrito.html", {
        "carrito": carrito,
        "total": carrito.total(),
    })