from django.contrib import admin
from .models import StoreConfig


@admin.register(StoreConfig)
class StoreConfigAdmin(admin.ModelAdmin):
    list_display = ("__str__", "is_open", "closed_message")

    def has_add_permission(self, request):
        # Only one record can exist
        return not StoreConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False