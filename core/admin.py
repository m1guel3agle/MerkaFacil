from django.contrib import admin
from .models import ConfigTienda

@admin.register(ConfigTienda)
class ConfigTiendaAdmin(admin.ModelAdmin):
    list_display = ("__str__", "abierta", "mensaje_cierre")

    def has_add_permission(self, request):
        # Solo puede existir un registro
        return not ConfigTienda.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False