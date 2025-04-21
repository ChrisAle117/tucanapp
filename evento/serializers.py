from .models import Evento
from rest_framework import serializers
from equipo.models import Equipo, Deporte



from rest_framework import serializers
from .models import Evento

class EventoSerializer(serializers.ModelSerializer):
    deporte_nombre = serializers.CharField(source='deporte.nombre', read_only=True)
    resultado_equipo = serializers.SerializerMethodField()
    class Meta:
        model = Evento
        fields = '__all__'

    def validate(self, data):
        if data['equipo1'].deporte != data['equipo2'].deporte:
            raise serializers.ValidationError("Los equipos deben ser del mismo deporte")
        if data['equipo1'] == data['equipo2']:
            raise serializers.ValidationError("Un equipo no puede jugar contra sí mismo")
        return data
    
    
    def get_resultado_equipo(self, obj):
        equipo_id = self.context.get('equipo_id')  # Obtener el ID del equipo desde el contexto
        if not equipo_id:
            return None

        
        if obj.puntos_equipo1 is None or obj.puntos_equipo2 is None:
                return "Resultado pendiente"

        if obj.equipo1.id == equipo_id:
                if obj.puntos_equipo1 > obj.puntos_equipo2:
                    return "Victoria"
                elif obj.puntos_equipo1 < obj.puntos_equipo2:
                    return "Derrota"
                else:
                    return "Empate"
        elif obj.equipo2.id == equipo_id:
                if obj.puntos_equipo2 > obj.puntos_equipo1:
                    return "Victoria"
                elif obj.puntos_equipo2 < obj.puntos_equipo1:
                    return "Derrota"
                else:
                    return "Empate"
        return None
