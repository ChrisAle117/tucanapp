from django.utils import timezone
from django.db import models
from django.forms import ValidationError

from equipo.models import Equipo
from deporte.models import Deporte

class Evento(models.Model):
    nombre = models.CharField(max_length=45)
    fecha = models.DateTimeField(default=timezone.now)
    equipo1 = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name='eventos_como_equipo1'
    )
    equipo2 = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name='eventos_como_equipo2'
    )

    deporte = models.ForeignKey(
        Deporte,
        on_delete=models.CASCADE,
        related_name='eventos',
        null=True, 
        blank=True  
    )

    puntos_equipo1 = models.IntegerField(null=True, blank=True)
    puntos_equipo2 = models.IntegerField(null=True, blank=True)
    resultado = models.CharField(max_length=225, blank=True, null=True)

    def calcular_resultado(self):
        if self.puntos_equipo1 > self.puntos_equipo2:
            return f"Ganador: {self.equipo1.nombre}"
        elif self.puntos_equipo1 < self.puntos_equipo2:
            return f"Ganador: {self.equipo2.nombre}"
        else:
            return "Empate"

    def __str__(self):
        return f"{self.equipo1} vs {self.equipo2} - {self.fecha}"

    def clean(self):
        if self.equipo1.deporte != self.equipo2.deporte:
            raise ValidationError("Los equipos deben ser del mismo deporte")
        if self.equipo1 == self.equipo2:
            raise ValidationError("Un equipo no puede jugar contra sí mismo")
        if self.puntos_equipo1 is not None and self.puntos_equipo1 < 0:
            raise ValidationError("Los puntos del equipo 1 no pueden ser negativos")
        if self.puntos_equipo2 is not None and self.puntos_equipo2 < 0:
            raise ValidationError("Los puntos del equipo 2 no pueden ser negativos")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)