from django.db import models
from django.forms import ValidationError

from equipo.models import Equipo
from posicion.models import Posicion
from datetime import date as Date

class Jugador(models.Model):
    nombre = models.CharField(max_length=45)
    edad = models.IntegerField()
    fecha_nacimiento = models.DateField()
    puntaje_mvp = models.FloatField(blank=True, null=True)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    es_titular = models.BooleanField(default=False)
    posicion = models.ForeignKey(Posicion, on_delete=models.RESTRICT)
    
    def clean(self):
        if self.posicion.deporte != self.equipo.deporte:
            raise ValidationError('La posición no corresponde al deporte del equipo')
        if self.edad < 0:
            raise ValidationError('La edad no puede ser negativa')
        if self.puntaje_mvp < 0:
            raise ValidationError('El puntaje MVP no puede ser negativo')
        if self.puntaje_mvp > 10:
            raise ValidationError('El puntaje MVP no puede ser mayor a 10')
        if self.fecha_nacimiento > Date.today():
            raise ValidationError('La fecha de nacimiento no puede ser mayor a la fecha actual')
        if self.edad < 0:
            raise ValidationError('La edad no puede ser negativa')
        
    def __str__(self):
        return f"{self.nombre} - {self.equipo.nombre}"
