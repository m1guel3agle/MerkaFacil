from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products.models import Product
from .models import Favorite


def home(request):
    products_preview = Product.objects.all()[:8]
    return render(request, "home.html", {"productos_preview": products_preview})


def about(request):
    return render(request, "about.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"].strip()
        password = request.POST["password"]
        username_exists = User.objects.filter(username=username).exists()
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect("/admin/")
            return redirect("home")

        error = (
            "La contraseña es incorrecta."
            if username_exists else
            "Ese usuario no está registrado. Primero debes crear una cuenta."
        )
        return render(request, "login.html", {
            "error": error,
            "username_value": username,
        })

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Ese nombre de usuario ya está en uso."
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        return redirect("login")

    return render(request, "signup.html")


@login_required
@require_POST
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    fav, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        fav.delete()
        return JsonResponse({"status": "removed", "message": f"{product.name} eliminado de favoritos."})
    return JsonResponse({"status": "added", "message": f"{product.name} agregado a favoritos."})


@login_required
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related("product")
    return render(request, "favorites.html", {"favorites": favorites})
