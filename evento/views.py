from .models import Evento
from .serializers import EventoSerializer
from rest_framework.exceptions import ValidationError

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now
from rest_framework import status
from .models import Deporte
from django.shortcuts import get_object_or_404

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    renderer_classes = [JSONRenderer]

    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['GET']:
            return []
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def listar_eventos(self, request):


        proximos_eventos = Evento.objects.filter(fecha__gt=now()).order_by('fecha')[:10]

        eventos_finalizados_serializados = self.get_serializer(eventos_finalizados, many=True).data
        proximos_eventos_serializados = self.get_serializer(proximos_eventos, many=True).data


        return Response({
            'proximosEventos': proximos_eventos_serializados,
            'eventosFinalizados': eventos_finalizados_serializados
        })
    
    def create(self, request, *args, **kwargs):
        data = request.data
        print(f"Datos recibidos: {data}")

        deporte_id = data.get('deporte')
        if not deporte_id:
            return Response({'error': 'El campo deporte es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)

        deporte = get_object_or_404(Deporte, id=deporte_id)
        print(f"Deporte encontrado: {deporte}")

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

    def save(self, *args, **kwargs):
        self.clean()
        self.deporte = self.equipo1.deporte
        super().save(*args, **kwargs)

    def perform_update(self, serializer):
        try:
            instance = serializer.save()
            instance.resultado = instance.calcular_resultado()
            instance.save()
        except ValidationError as e:
            raise ValidationError({"detail": str(e)})

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.db.models import Q


@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@api_view(['GET'])
def evento_list(request, pk):
    eventos = Evento.objects.filter(Q(equipo1=pk) | Q(equipo2=pk))
    serializer = EventoSerializer(eventos, many=True)
    return Response({'eventos': serializer.data}, status=200)