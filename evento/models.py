from django.utils import timezone
from django.db import models
from django.forms import ValidationError


from equipo.models import Equipo

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
    puntos_equipo1 = models.PositiveIntegerField(default=0)
    puntos_equipo2 = models.PositiveIntegerField(default=0)

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


    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)