from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("Rango says: Hello World ! <a href ='/rango/about'>About</a>")

def about(request):
    return HttpResponse("Rango says: Here is about page...  <a href = '/rango/index'>Index</a>")

