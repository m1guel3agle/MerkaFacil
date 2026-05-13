from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import StoreConfig


@admin.register(StoreConfig)
class StoreConfigAdmin(admin.ModelAdmin):
    list_display = ("__str__", "status_badge", "closed_message")
    readonly_fields = ()

    @admin.display(description="Estado")
    def status_badge(self, obj):
        if obj.is_open:
            return mark_safe('<span style="color:#2E7D32;font-weight:bold;">&#x2713; Abierta</span>')
        return mark_safe('<span style="color:#c62828;font-weight:bold;">&#x2715; Cerrada</span>')

    def has_add_permission(self, _request):
        return not StoreConfig.objects.exists()

    def has_delete_permission(self, _request, _obj=None):
        return False
