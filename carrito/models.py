from django.db import models
from django.contrib.auth.models import User


class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=0)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f'Pedido #{self.id} — {self.usuario.username}'


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto_id = models.IntegerField()
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    cantidad = models.IntegerField()
    imagen = models.CharField(max_length=500, blank=True)

    def subtotal(self):
        return self.precio * self.cantidad

    def __str__(self):
        return f'{self.nombre} x{self.cantidad}'