from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .carrito import Carrito
from .models import Pedido, ItemPedido
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


@login_required
def realizar_compra(request):
    if request.method == "POST":
        carrito = Carrito(request)

        if not carrito.carrito:
            return redirect("carrito")

        pedido = Pedido.objects.create(
            usuario=request.user,
            total=carrito.total(),
        )

        for item in carrito:
            ItemPedido.objects.create(
                pedido=pedido,
                producto_id=item["producto_id"],
                nombre=item["nombre"],
                precio=item["precio"],
                cantidad=item["cantidad"],
                imagen=item.get("imagen", ""),
            )

        carrito.limpiar()
        return redirect("confirmacion_pedido", pedido_id=pedido.id)

    return redirect("carrito")


@login_required
def confirmacion_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    return render(request, "carrito/confirmacion.html", {"pedido": pedido})


@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    return render(request, "carrito/pedidos.html", {"pedidos": pedidos})