from django.db import models

class ConfigTienda(models.Model):
    abierta = models.BooleanField(default=True)
    mensaje_cierre = models.CharField(
        max_length=255,
        default="La tienda está cerrada en este momento. ¡Vuelve pronto!"
    )

    class Meta:
        verbose_name = "Configuración de tienda"
        verbose_name_plural = "Configuración de tienda"

    def __str__(self):
        return "Abierta" if self.abierta else "Cerrada"

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj