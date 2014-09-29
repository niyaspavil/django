from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.http import HttpResponse


def index(request):
     
  
    return 

def about(request):
    return HttpResponse("Rango says: Here is about page...  <a href = '/rango/index'>Index</a>")

