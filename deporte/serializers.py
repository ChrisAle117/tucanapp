from .models import Deporte
from rest_framework import serializers
import re

class DeporteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    max_titulares = serializers.IntegerField(source='configuraciondeporte.max_titulares', read_only=True)
    max_suplentes = serializers.IntegerField(source='configuraciondeporte.max_suplentes', read_only=True)

    class Meta:
        model = Deporte
        fields = ['id', 'nombre', 'max_titulares', 'max_suplentes']


    def validate_nombre(self, value):
        if not re.match(r'^[a-zA-Z0-9\s]+$', value):
            raise serializers.ValidationError("El nombre solo puede contener letras, números y espacios.")
        return value

    
    def create(self, validated_data):
        
        deporte = Deporte.objects.create(**validated_data)
        return deporte

    def update(self, instance, validated_data):
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
