from .models import Evento
from rest_framework import serializers
from equipo.models import Equipo, Deporte



from rest_framework import serializers
from .models import Evento

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'

    def validate_deporte(self, value):
        if not Deporte.objects.filter(pk=value).exists():
            raise serializers.ValidationError("El deporte especificado no existe.")
        return value

    def validate(self, data):
        if data['equipo1'].deporte != data['equipo2'].deporte:
            raise serializers.ValidationError("Los equipos deben ser del mismo deporte")
        if data['equipo1'] == data['equipo2']:
            raise serializers.ValidationError("Un equipo no puede jugar contra sí mismo")
        return data
    
