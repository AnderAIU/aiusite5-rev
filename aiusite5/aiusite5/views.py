from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.template import Template, Context
from django.http import HttpResponse
from django.shortcuts import redirect
from aiupages.models import *
from aiupages.views import pageshtml
from aiucolors.models import *
from aiuextended.models import AiuExtParam
#import pdb
#from logs.models import Post

def page_index(request):    
    name_page = request.GET.get("name")
    if name_page == 'home': 
        return redirect('/', permanent=True) #redirect / убрать лишние запросы
    context = pageshtml(name_page)
    #context["pos"] = color_profile.objects.first()
    return render(request, 'base/page.html', context)

#no optimized
def pageNotFound(request, exception):
    context = pageshtml('404')
    context["deb"] = '404'
    response = render(request, 'base/page.html', context)
    response.status_code = 404
    return response

def getMac(request):
    context = Context()
    response = render(request, Template('OK'), context)
    response.status_code = 200
    return response