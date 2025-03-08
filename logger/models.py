from django.db import models

class Logger(models.Model):
    TIPO_MOVIMIENTO = (
        ('INSERT', 'Inserción'),
        ('UPDATE', 'Actualización'),
        ('DELETE', 'Eliminación'),
        ('LOGIN', 'Inicio de sesión'),
        ('OTHER', 'Otro'),
    )
    
    nombre_dato = models.CharField(max_length=100)
    tipo_movimiento = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO)
    valores = models.JSONField()
    fecha_hora = models.DateTimeField(auto_now_add=True)
    host_origen = models.CharField(max_length=45)
    usuario = models.CharField(max_length=45)
    
    def __str__(self):
        return f"{self.tipo_movimiento} en {self.nombre_dato}"
