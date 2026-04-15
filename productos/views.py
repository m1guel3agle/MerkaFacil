from django.shortcuts import render
from .models import Product
from core.models import StoreConfig


def catalog(request):
    products = Product.objects.all()
    store = StoreConfig.get()
    return render(request, "products.html", {
        "products": products,
        "store_open": store.is_open,
        "closed_message": store.closed_message,
    })