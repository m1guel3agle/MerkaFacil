from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from productos.models import Product


def home(request):
    products_preview = Product.objects.all()[:8]
    return render(request, "home.html", {"productos_preview": products_preview})


def about(request):
    return render(request, "about.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {
                "error": "Usuario o contraseña incorrectos."
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
            password=password
        )
        return redirect("login")

    return render(request, "signup.html")
