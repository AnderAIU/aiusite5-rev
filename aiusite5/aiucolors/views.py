from django.shortcuts import render
from .models import color_profile
from aiupages.models import *

# Create your views here.
def css_renderer(request, filename):
    context = dict()
    context["colors"] = color_profile.objects.first()
    return render(request, filename + '.css', context, content_type="text/css")

def js_renderer(request, filename, slug):
    context = dict()
    context["colors"] = color_profile.objects.first()
    if slug == '':
        slug = 'home'
    context["aiupages"] = Pages.objects.filter(slug=slug)
    return render(request, filename + '.js', context, content_type="text/javascript")