from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.http import FileResponse
import json
import io
from reportlab.pdfgen import canvas

# Create your views here.

def page_test(request):
    context = dict()
    return render(request, 'base/blocks/opendoc.html', context)