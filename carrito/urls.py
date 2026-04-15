from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_cart, name="cart"),
    path("add/<int:product_id>/", views.add_product, name="add"),
    path("remove-one/<int:product_id>/", views.remove_one, name="remove_one"),
    path("remove/<int:product_id>/", views.remove_product, name="remove"),
    path("clear/", views.clear_cart, name="clear_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("confirmation/<int:order_id>/", views.order_confirmation, name="order_confirmation"),
    path("orders/", views.my_orders, name="my_orders"),
]