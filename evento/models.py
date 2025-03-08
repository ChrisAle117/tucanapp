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
    resultado = models.CharField(max_length=45, blank=True, null=True)
    
    def clean(self):
        if self.equipo1.deporte != self.equipo2.deporte:
            raise ValidationError('Los equipos deben ser del mismo deporte')
        if self.equipo1 == self.equipo2:
            raise ValidationError('Un equipo no puede jugar contra sí mismo')
    
    def __str__(self):
        return f"{self.equipo1} vs {self.equipo2} - {self.fecha}"
