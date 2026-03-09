from django.shortcuts import redirect, render
from .carrito import Carrito
from productos.models import Producto


def agregar_producto(request, producto_id):

    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)

    carrito.agregar(producto)

    return redirect("productos")


def ver_carrito(request):

    return render(request, "carrito/carrito.html")