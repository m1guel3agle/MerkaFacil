from django.urls import path
from . import views

urlpatterns = [
    path("", views.ver_carrito, name="carrito"),
    path("agregar/<int:producto_id>/", views.agregar_producto, name="agregar"),
    path("restar/<int:producto_id>/", views.restar_producto, name="restar"),
    path("eliminar/<int:producto_id>/", views.eliminar_producto, name="eliminar"),
    path("limpiar/", views.limpiar_carrito, name="limpiar_carrito"),
    path("comprar/", views.realizar_compra, name="realizar_compra"),
    path("confirmacion/<int:pedido_id>/", views.confirmacion_pedido, name="confirmacion_pedido"),
    path("pedidos/", views.mis_pedidos, name="mis_pedidos"),
]