from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return Httpresponse("Rango says hello to you")
