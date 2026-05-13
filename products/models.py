from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción",
        help_text="Descripción del producto visible al hacer clic en la tarjeta.",
    )
    price = models.IntegerField()
    stock = models.IntegerField()
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    def __str__(self):
        return self.name