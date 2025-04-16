from .models import ConfiguracionDeporte
from rest_framework import serializers
from deporte.models import Deporte
from deporte.serializers import DeporteSerializer

class ConfiguracionDeporteSerializer(serializers.ModelSerializer):
    deporte = DeporteSerializer()

    class Meta:
        model = ConfiguracionDeporte
        fields = '__all__'
    
    def create(self, validated_data):
        # Extraer los datos del deporte
        deporte_data = validated_data.pop('deporte')
        # Crear el objeto Deporte
        deporte = Deporte.objects.create(**deporte_data)
        # Crear la configuración del deporte con el deporte recién creado
        configuracion_deporte = ConfiguracionDeporte.objects.create(deporte=deporte, **validated_data)
        return configuracion_deporte
    
    def update(self, instance, validated_data):
        # Extraer los datos del deporte
        deporte_data = validated_data.pop('deporte', None)

        # Actualizar los datos del deporte si existen
        if deporte_data:
            deporte_instance = instance.deporte
            for attr, value in deporte_data.items():
                setattr(deporte_instance, attr, value)
            deporte_instance.save()

        # Actualizar los datos de ConfiguracionDeporte
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance