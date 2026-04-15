from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_id', 'name', 'price', 'quantity', 'image')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'total', 'status')
    list_filter = ('status',)
    list_editable = ('status',)
    inlines = [OrderItemInline]