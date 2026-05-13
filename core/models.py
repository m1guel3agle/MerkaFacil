from django.db import models
from django.contrib.auth.models import User


class StoreConfig(models.Model):
    is_open = models.BooleanField(default=True)
    closed_message = models.CharField(
        max_length=255,
        default="The store is currently closed. Come back soon!"
    )

    class Meta:
        verbose_name = "Store Configuration"
        verbose_name_plural = "Store Configuration"

    def __str__(self):
        return "Open" if self.is_open else "Closed"

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    product = models.ForeignKey(
        "productos.Product", on_delete=models.CASCADE, related_name="favorited_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username} → {self.product.name}"