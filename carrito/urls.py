from django.urls import path
from . import views

urlpatterns = [

    path("agregar/<int:producto_id>/", views.agregar_producto, name="agregar"),
    path("", views.ver_carrito, name="carrito"),

]