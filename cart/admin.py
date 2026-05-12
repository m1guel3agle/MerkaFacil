from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_id", "name", "price", "quantity", "image", "subtotal")
    fields = ("name", "quantity", "price", "subtotal", "image")

    @admin.display(description="Subtotal")
    def subtotal(self, obj):
        return f"${obj.subtotal():,}"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date", "total_fmt", "delivery_method", "payment_method", "status")
    list_display_links = ("id", "user")
    list_filter = ("status", "delivery_method", "payment_method")
    list_editable = ("status",)
    search_fields = ("user__username", "user__email")
    date_hierarchy = "date"
    readonly_fields = ("date", "total")
    inlines = [OrderItemInline]

    @admin.display(description="Total", ordering="total")
    def total_fmt(self, obj):
        return f"${obj.total:,.0f}"
