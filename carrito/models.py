from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("processing", "En proceso"),
        ("delivered", "Entregado"),
        ("cancelled", "Cancelado"),
    ]

    DELIVERY_CHOICES = [
        ("pickup", "Recoger en la tienda"),
        ("delivery", "Delivery"),
    ]

    PAYMENT_CHOICES = [
        ("cash", "Efectivo"),
        ("card", "Tarjeta"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES, null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, null=True, blank=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_id = models.IntegerField()
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.IntegerField()
    image = models.CharField(max_length=500, blank=True)

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.name} x{self.quantity}"