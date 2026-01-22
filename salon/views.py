from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Привет из приложения salon!")
