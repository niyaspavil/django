from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.http import HttpResponse

# import rango model

from rango.models import Category

def index(request):
     
    context = RequestContext(request)
    
    category_list = Catogory.objects.order('likes')[:5]
    context_dict = {"categories": category_list}
    
    return render_to_response('rango/index.html',context_dict,context)

def about(request):
    
    context = RequestContext(request)
    context_dict = {"boldmessage": " i am bold font from the context"}
    
    return render_to_response('rango/about.html',context_dict,context)


