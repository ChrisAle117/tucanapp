from django.contrib import admin
from django.urls import path, include
from app.views import *
from users.views import * 

urlpatterns = [
    path('usuarios/', include('users.urls')),
    path('equipos/', include('equipo.urls')),
    path('deportes/', include('deporte.urls')),
    path('eventos/', include('evento.urls')),
    path('config_deporte/', include('configuracion_deporte.urls')),
    path('posicion/', include('posicion.urls')),
    path('jugadores/', include('jugador.urls')),
    path('' , index, name='index'),
    path('login/' , login_view, name='login'),
    path('logout/' , logout_view, name='logout'),

]