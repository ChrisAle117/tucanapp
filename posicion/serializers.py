from .models import Posicion
from rest_framework import serializers
import re

class PosicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posicion
        fields = '__all__'
        
    def validate_nombre(self, value):
        if not re.match(r'^[a-zA-Z\s]+$', value):
            raise serializers.ValidationError("El nombre solo puede contener letras y espacios.")
        return value