from .models import ConfiguracionDeporte
from rest_framework import serializers

class ConfiguracionDeporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionDeporte
        fields = '__all__'
