from django.urls import path
from . import views
from .views import login_view, logout_view, signup_view

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("signup/", signup_view, name="signup"),
    path("favorites/toggle/<int:product_id>/", views.toggle_favorite, name="toggle_favorite"),
    path("favorites/mis-favoritos/", views.my_favorites, name="my_favorites"),
]