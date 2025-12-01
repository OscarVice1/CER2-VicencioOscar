from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User


class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    fecha_hora = models.DateTimeField()
    lugar = models.CharField(max_length=100)
    imagen_tarjeta = models.ImageField(upload_to="eventos/tarjetas")
    imagen_banner = models.ImageField(upload_to="eventos/banner", blank=True, null=True)
    valor = models.DecimalField(max_digits=6, decimal_places=0)
    plazas_disponibles = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["lugar", "fecha_hora"], name="evento_unico_fecha_lugar"
            ),
            models.CheckConstraint(
                check=Q(plazas_disponibles__gte=0), name="plazas_no_negativas"
            ),
            models.CheckConstraint(check=Q(valor__gte=0), name="precio_no_negativo"),
        ]

    def __str__(self):
        return self.titulo


class Asistente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "evento"], name="registro_unico_evento_usuario"
            )
        ]

    def __str__(self):
        return f"{self.usuario.username}"
