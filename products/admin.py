from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock", "has_image")
    list_display_links = ("name",)
    list_editable = ("price", "stock")
    search_fields = ("name",)
    list_filter = ("stock",)
    ordering = ("name",)

    @admin.display(boolean=True, description="Imagen")
    def has_image(self, obj):
        return bool(obj.image)
