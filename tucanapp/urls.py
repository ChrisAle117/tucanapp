from django.contrib import admin
from django.urls import path, include
from app.views import *
from users.views import * 

urlpatterns = [
    path('usuarios/', include('users.urls')),
    path('' , index, name='index'),
    path('login/' , login_view, name='login'),
    path('logout/' , logout_view, name='logout'),
]
