from .models import Evento
from .serializers import EventoSerializer
from rest_framework.exceptions import ValidationError

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import is_naive
from rest_framework.response import Response
from django.utils.timezone import now
from rest_framework import status
from equipo.models import Equipo

from datetime import datetime, timedelta
from django.utils.timezone import make_aware

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    renderer_classes = [JSONRenderer]

    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [IsAuthenticated()]  

    def create(self, request, *args, **kwargs):
        data = request.data

        deporte_id = data.get('deporte')
        if not deporte_id:
            return Response({'error': 'El campo deporte es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)

        fecha_evento = data.get('fecha')
        if not fecha_evento:
            return Response({'error': 'El campo fecha es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)

        equipo1_id = data.get('equipo1')
        equipo2_id = data.get('equipo2')

        if not equipo1_id or not equipo2_id:
            return Response({'error': 'Ambos equipos son obligatorios.'}, status=status.HTTP_400_BAD_REQUEST)

          # Importar el modelo Equipo
        try:
            equipo1 = Equipo.objects.get(id=equipo1_id)
            equipo2 = Equipo.objects.get(id=equipo2_id)
        except Equipo.DoesNotExist:
            return Response({'error': 'Uno o ambos equipos no existen.'}, status=status.HTTP_400_BAD_REQUEST)

        if not equipo1.activo or not equipo2.activo:
            return Response({'error': 'No se pueden crear eventos con equipos inactivos.'}, status=status.HTTP_400_BAD_REQUEST)

        current_time = now()
        limite_fecha = current_time - timedelta(days=6)


        try:
            fecha_evento_obj = datetime.fromisoformat(fecha_evento.replace("Z", "+00:00"))
            fecha_evento_obj = make_aware(fecha_evento_obj) 
        except ValueError:
            return Response({'error': 'El formato de la fecha es inválido. Use el formato ISO 8601.'}, status=status.HTTP_400_BAD_REQUEST)

        if fecha_evento_obj < limite_fecha:
            return Response(
                {'error': 'No se pueden agregar eventos con una fecha mayor a 6 días en el pasado.'},
                status=status.HTTP_400_BAD_REQUEST
            )


        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
def perform_update(self, serializer):
    try:
        instance = serializer.save()
        current_time = now()
        limite_fecha = current_time - timedelta(days=6)

        print(f"Current time: {current_time}")
        print(f"Límite de fecha: {limite_fecha}")
        print(f"Fecha del evento (antes de procesar): {instance.fecha}")

        if not instance.fecha:
            raise ValidationError({"detail": "El campo 'fecha' no puede estar vacío."})

        try:
            fecha_evento_obj = datetime.fromisoformat(instance.fecha.isoformat())
            fecha_evento_obj = make_aware(fecha_evento_obj) if is_naive(fecha_evento_obj) else fecha_evento_obj
        except ValueError as e:
            raise ValidationError({"detail": f"Error al procesar la fecha del evento: {str(e)}"})

        print(f"Fecha del evento (con zona horaria): {fecha_evento_obj}")


        if fecha_evento_obj < limite_fecha:
            raise ValidationError({"detail": "No se puede actualizar un evento que ocurrió hace más de 6 días."})


        instance.resultado = instance.calcular_resultado()
        instance.save()

    except ValidationError as e:
        print(f"ValidationError: {e}")  
        raise ValidationError({"detail": str(e)})
    except Exception as e:
        print(f"Unexpected error: {e}")  
        raise ValidationError({"detail": f"Error inesperado: {str(e)}"})

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.db.models import Q


@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@api_view(['GET'])
def estadisticas_equipo(request, pk):

    eventos = Evento.objects.filter(Q(equipo1=pk) | Q(equipo2=pk))
    serializer = EventoSerializer(eventos, many=True, context={'equipo_id': pk})
    eventos_serializados = serializer.data

    victorias = sum(
        1 for evento in eventos_serializados
        if (evento['resultado_equipo'] == "Victoria" and evento['equipo1'] == pk and evento['puntos_equipo1'] > evento['puntos_equipo2']) or
           (evento['resultado_equipo'] == "Victoria" and evento['equipo2'] == pk and evento['puntos_equipo2'] > evento['puntos_equipo1'])
    )

    derrotas = sum(
        1 for evento in eventos_serializados
        if (evento['resultado_equipo'] == "Derrota" and evento['equipo1'] == pk and evento['puntos_equipo1'] < evento['puntos_equipo2']) or
           (evento['resultado_equipo'] == "Derrota" and evento['equipo2'] == pk and evento['puntos_equipo2'] < evento['puntos_equipo1'])
    )

    empates = sum(
        1 for evento in eventos_serializados
        if evento['resultado_equipo'] == "Empate" and evento['puntos_equipo1'] == evento['puntos_equipo2']
    )

    total_partidos = victorias + derrotas + empates
    efectividad = (victorias / total_partidos * 100) if total_partidos > 0 else 0


    efectividad = round(efectividad, 2)

    
    return Response({
        'eventos': eventos_serializados,
        'estadisticas': {
            'victorias': victorias,
            'derrotas': derrotas,
            'empates': empates,
            'efectividad': efectividad
        }
    }, status=200)