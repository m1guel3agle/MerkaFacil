from django.shortcuts import render
from .models import Producto
from core.models import ConfigTienda

def catalogo(request):
    productos = Producto.objects.all()
    tienda = ConfigTienda.get()
    return render(request, "productos.html", {
        "productos": productos,
        "tienda_abierta": tienda.abierta,
        "mensaje_cierre": tienda.mensaje_cierre,
    })