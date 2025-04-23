from .models import Equipo
from .serializers import EquipoSerializer
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status


from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from jugador.models import Jugador  
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from evento.models import Evento
from django.db.models import Q

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer
    renderer_classes = [JSONRenderer]

    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
    # Forzar que el equipo se cree con el estado activo
        serializer.save(activo=True)

    def get_permissions(self):
        # Permitir acceso público para solicitudes GET
        if self.request.method == 'GET':
            return []  # Sin autenticación para GET
        return [IsAuthenticated()]  # Requiere autenticación para otros métodos
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        # Obtener el equipo actual
        equipo = self.get_object()
        jugadores_asociados = Jugador.objects.filter(equipo=equipo).exists()

        # Verificar si el deporte está siendo modificado
        if 'deporte' in request.data and request.data['deporte'] != str(equipo.deporte.id):
            if jugadores_asociados:
                return Response(
                    {"error": "No se puede cambiar el deporte de un equipo que ya tiene jugadores registrados."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            eventos_asociados = Evento.objects.filter(Q(equipo1=equipo) | Q(equipo2=equipo)).exists()
            if eventos_asociados:
                return Response(
                    {"error": "No se puede cambiar el deporte de un equipo que ya tiene o tuvo eventos asociados."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Si pasa la validación, proceder con la actualización
        return super().update(request, *args, **kwargs)
    def post(self, request):
        serializer = EquipoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        estado = self.request.query_params.get('activo', None)
        if estado is not None:
            if estado.lower() == 'true':
                return Equipo.objects.filter(activo=True)
            elif estado.lower() == 'false':
                return Equipo.objects.filter(activo=False)
        return Equipo.objects.all()  # D

    @action(detail=True, methods=['post'], url_path='cambiar_estado')
    def cambiar_estado(self, request, pk=None):
        equipo = self.get_object()
        equipo.activo = not equipo.activo
        try:
            equipo.save()
            return Response({'status': 'Estado actualizado', 'activo': equipo.activo})
        except ValidationError as e:
            return Response({'error': e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
  
        
        