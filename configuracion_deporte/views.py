from .models import ConfiguracionDeporte
from .serializers import ConfiguracionDeporteSerializer
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class ConfiguracionDeporteViewSet(viewsets.ModelViewSet):
    queryset = ConfiguracionDeporte.objects.all()
    serializer_class = ConfiguracionDeporteSerializer
    renderer_classes = [JSONRenderer]

    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['GET','POST','PUT', 'DELETE']:
            return [IsAuthenticated()]
        return []
    
