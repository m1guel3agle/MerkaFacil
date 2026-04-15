from django.db import models


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