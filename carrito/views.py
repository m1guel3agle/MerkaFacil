from django.shortcuts import redirect, render
from .carrito import Carrito
from productos.models import Producto


def agregar_producto(request, producto_id):

    carrito = request.session.get("carrito", [])

    carrito.append(producto_id)

    request.session["carrito"] = carrito

    return redirect("catalogo")


def ver_carrito(request):

    return render(request, "carrito/carrito.html")