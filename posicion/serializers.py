from .models import Posicion
from rest_framework import serializers
import re

class PosicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posicion
        fields = '__all__'
        
    def validate_nombre(self, value):
        if not re.match(r'^[A-Za-z0-9_ ]+$', value):  # Se agregó el espacio al patrón
            raise serializers.ValidationError("El nombre solo puede contener letras, números, guiones bajos y espacios.")
        return value