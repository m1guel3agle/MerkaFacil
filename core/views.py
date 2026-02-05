from django.shortcuts import render

def home(request):
    return render(request, "home.html")
def about(request):
    return render(request, "about.html")

def productos(request):
    productos = [
        {"nombre": "Arroz", "precio": 2500, "stock": 20},
        {"nombre": "Leche", "precio": 3800, "stock": 12},
        {"nombre": "Pan", "precio": 500, "stock": 50},
    ]
    return render(request, "productos.html", {"productos": productos})
