from django.db import models

class Deporte(models.Model):
    nombre = models.CharField(max_length=45, unique=True)
    
    def __str__(self):
        return self.nombre
