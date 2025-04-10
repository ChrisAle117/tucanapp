from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
#Falta importar el modelo
from .models import CustomUser
#Falta importar el serializador
from .serializers import CustomUserSerializer
from rest_framework.renderers import JSONRenderer

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.decorators import login_required

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    renderer_classes = [JSONRenderer]

    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['GET','POST','PUT', 'DELETE']:
            # Checar si tenemos sesión 
            return [IsAuthenticated()]


from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
# Quito el decorador de csrf 

class CustomUserFormAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request, *args, **kwargs):
        try:
            user_data = json.loads(request.body)
            User = get_user_model()
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                nombre=user_data['nombre'],
                apellidos=user_data['apellidos'],
                rol=user_data['rol'],
                detalles=user_data['detalles']
            )
            return Response({'message': 'Usuario creado con éxito'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': f'Error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


def dashboard(request):
    return render(request, 'dashboard.html')

from django.contrib.auth import  logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from .message import message as Message

def login_view(request):
    return render(request, 'login.html')

def logout_view(request):
    logout(request)

    message = Message(
        type="info",
        message="Se ha cerrado la sesión exitosamente",
        code=200,
        img="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR8MIbugIhZBykSmQcR0QPcfnPUBOZQ6bm35w&s"
    )
    return render(request, "login.html", {"message": json.dumps(message.to_dict())})

@login_required
def home_view(request):
    return render(request, 'home.html')

