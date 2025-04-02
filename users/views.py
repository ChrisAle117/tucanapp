from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
#Falta importar el modelo
from .models import CustomUser
#Falta importar el serializador
from .serializers import CustomUserSerializer
from rest_framework.renderers import JSONRenderer


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


from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class CustomUserFormAPI(APIView):
    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        fields = {
            field: {
            'label': form[field].label,
            'input':form[field].field.widget.attrs,
            'type': form[field].field.widget.input_type,
            }
                for field in form.fields
        }
        return Response(fields)

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.data)
        if form.is_valid():
            user_data = form.cleaned_data
            User = get_user_model()
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password1'],
                nombre=user_data['nombre'],
                apellidos=user_data['apellidos'],
                rol=user_data['rol'],
                detalles=user_data['detalles']
            )
            return Response({'message': 'Usuario creado con éxito'},status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponseRedirect
from django.urls import reverse

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            message = Message(
                type="success",
                message="Usuario creado con éxito",
                code=200,
                img="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR8MIbugIhZBykSmQcR0QPcfnPUBOZQ6bm35w&s"
            )
            return render(request, 'login.html', {"message": json.dumps(message.to_dict())})
    else:
        form = CustomUserCreationForm()
    return render(request, 'registro.html', {'form': form})

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

