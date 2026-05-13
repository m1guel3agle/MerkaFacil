from django.shortcuts import render
from .models import Product
from core.models import StoreConfig


def catalog(request):
    products = Product.objects.all()
    store = StoreConfig.get()
    favorite_ids = set()
    if request.user.is_authenticated:
        from core.models import Favorite
        favorite_ids = set(
            Favorite.objects.filter(user=request.user).values_list("product_id", flat=True)
        )
    return render(request, "products.html", {
        "products": products,
        "store_open": store.is_open,
        "closed_message": store.closed_message,
        "favorite_ids": favorite_ids,
    })
