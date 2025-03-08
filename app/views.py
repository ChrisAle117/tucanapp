from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from .models import ErrorLog


def index(request):
    return render(request, 'index.html', status=200)

def show_error_404(request):
    return render(request, '404.html', status=404)

def show_error_505(request):
    return render(request, '505.html', status=505)

def generar_error(request):
    return 7/0
