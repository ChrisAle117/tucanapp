
from django.db import models



class Usuario(models.Model):
    ROLES = (
        ('dueño', 'Dueño'),
        ('admin', 'Administrador'),
        ('entrenador', 'Entrenador'),
    )
    
    username = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=255)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=50)
    rol = models.CharField(max_length=10, choices=ROLES)
    detalles = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellidos} ({self.rol})"