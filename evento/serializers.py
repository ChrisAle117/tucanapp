from .models import Evento
from rest_framework import serializers
from equipo.models import Equipo, Deporte



from rest_framework import serializers
from .models import Evento

class EventoSerializer(serializers.ModelSerializer):
    deporte_nombre = serializers.CharField(source='deporte.nombre', read_only=True)
    class Meta:
        model = Evento
        fields = '__all__'

    def validate(self, data):
        if data['equipo1'].deporte != data['equipo2'].deporte:
            raise serializers.ValidationError("Los equipos deben ser del mismo deporte")
        if data['equipo1'] == data['equipo2']:
            raise serializers.ValidationError("Un equipo no puede jugar contra sí mismo")
        return data
    
