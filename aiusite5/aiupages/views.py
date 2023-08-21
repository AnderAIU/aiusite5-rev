from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from wsgiref.util import FileWrapper
from django.template import Template, Context
from aiupages.models import *
from aiucolors.models import color_profile
from django.views.generic import ListView, DetailView
from django.db.models import Q
import json
import requests

# Create your views here.

def outMac(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print('IP: '+ ip)
    print('Browser' + request.META.get('HTTP_USER_AGENT'))
    print('Browser' + request.META.get('HTTP_HOST'))
    return 'Connect clients IP:' + ip

def convertfile11(dirfile):
    basurl = 'http://62.217.177.31:9980/lool/convert-to/pdf'
    dirfile1 = '../public_html/' + dirfile
    filesin = {
        "data": open(dirfile1,'rb'),
    }
    r = requests.post(basurl, files=filesin)
    print(r)
    print(r.content)
    print(r.text)
    try:
        with open(dirfile+".pdf", "wb") as f:
            f.write(r.content)
        return dirfile+".pdf"
    except:
        return ''

class PageView(ListView):
    model = Pages
    template_name = 'base/page2.html'
    context_object_name = 'aiupage'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name_page = self.request.GET.get("name")
        if name_page is None or name_page == '' or name_page == '/':
            name_page = "home"
        context['aiupages'] = Pages.objects.filter(slug=name_page)
        if not(context['aiupages']):
            name_page = "404"
            context['aiupages'] = Pages.objects.filter(slug=name_page)
        context['slug'] = name_page
        context["pos"] = color_profile.objects.first()
        return context

def get_pages(request):
    print(outMac(request))
    name_page = request.GET.get("name")
    if name_page is None or name_page == '' or name_page == '/':
        name_page = "home"
    context = Context()
    context['aiupages'] = Pages.objects.filter(slug=name_page)
    if not(context['aiupages']):
        name_page = "404"
        context['aiupages'] = Pages.objects.filter(slug=name_page)
    context["pos"] = color_profile.objects.first()
    template1 = Template('{% extends "base/content.html" %}')
    template2 = Template('{{ aiupages.last.public_name|upper }}')
    if (Template('{{ aiupages.first.fullmenu }}').render(context) == 'True'):
        tmp = 'full'
    elif (Template('{{ aiupages.first.fullmenu }}').render(context) == 'False'):
        tmp = 'normal'
    else:
        tmp = 'normal'
    data = []
    data.append({
        'title': Template('{{ aiupages.first.slug }}').render(context),
        'header': template2.render(context),
        'contenthtml': template1.render(context),
        'deb': name_page,
        'fullmenu': tmp,
    })
    return JsonResponse(data, safe=False)

#menu param
def get_param(request):
    print(outMac(request))
    name_page = request.GET.get("name")
    if name_page is None or name_page == '' or name_page == '/':
        name_page = "home"
    context = Context()
    context['aiupages'] = Pages.objects.filter(slug=name_page)
    if not(context['aiupages']):
        name_page = "404"
        context['aiupages'] = Pages.objects.filter(slug=name_page)
    data = []
    if (Template('{{ aiupages.first.fullmenu }}').render(context) == 'True'):
        tmp = 'full'
    elif (Template('{{ aiupages.first.fullmenu }}').render(context) == 'False'):
        tmp = 'normal'
    else:
        tmp = 'normal'
    print(tmp)
    data.append({
        'title': context["aiupages"].__str__(),
        'fullmenu': tmp,
    })
    return JsonResponse(data, safe=False)

#Files Upload
def get_files(request):
    inres = json.loads(request.body)
    tags = TagsItem.objects.filter(slug__in=inres["tags"])
    filesout = FilesUpload.objects.all()
    if bool(inres["slug"].strip()):
        pagesfile = Pages.objects.filter(slug=inres["slug"])
        for pg in pagesfile.all():
            filesout = filesout.filter(pageid=pg)
    for tag1 in tags.all():
        filesout = filesout.filter(tagsid=tag1)
    context = Context()
    context["aiufiles"] = filesout
    template1 = Template('{% extends "base/blocks/getfile.html" %}')
    data = []
    data.append({
        'files': template1.render(context),
    })
    return JsonResponse(data, safe=False)

def openfile(request):
    inres = json.loads(request.body)
    print(inres['fileurl'])
    context = Context()
    template1 = Template('{% extends "base/blocks/opendoc.html" %}')
    template2 = Template('{{ aiuopen }}')
    if (inres['mimefile'] == 'application/pdf'):
        context['aiuopen'] = '../public_html/' + inres['fileurl']
    elif (inres['mimefile'] == 'application/msword' or inres['mimefile'] == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
        print('Convertation ' + inres['fileurl'] + '....')
        context['aiuopen'] = ''
        print(context['aiuopen'])
    data = []
    data.append({
        'viewer': template1.render(context),
        'filesurl' : template2.render(context),
    })
    return JsonResponse(data, safe=False)

# tests
def pageshtml(namePage):
    context = Context()
    result = dict()
    np = namePage
    if np is None or np == '':
        np = 'home'
    result["aiupages"] = Pages.objects.filter(slug=np)
    if not(result["aiupages"]):
        result["aiupages"] = Pages.objects.filter(slug='404')
    context["pos"] = result["glob"] = color_profile.objects.first()
    context["aiucontainer"] = Containers.objects.filter(page_member__in=result["aiupages"]).order_by('order')
    contenthtml0 = ''
    for aiucont in context["aiucontainer"]:
        context["aiublock"] = Blocks.objects.filter(contid=aiucont).order_by('order')
        context["debug"] = aiucont
        for aiublocks2 in context["aiublock"]:
            context["debug"] = aiublocks2
            contexthtml1 = ''
            temp1 = ContactBlock.objects.filter(blockid=aiublocks2)
            temp2 = ModernBlock.objects.filter(blockid=aiublocks2)
            try:
                temp3 = TextBlock.objects.get(blockid=aiublocks2)
            except:
                temp3 = False
            if temp3:
                context["aiutextblock"] = temp3
                contexthtml1 += Template('{% extends "base/blocks/textblock.html" %}').render(context)
            if temp2:
                context["aiucontact"] = ContactBlock.objects.filter(blockid=aiublocks2)
                #contexthtml1 += Template('{% extends "base/blocks/contact.html" %}').render(context)
            if temp1:
                context["modernui"] = ModernBlock.objects.filter(blockid=aiublocks2)
                context["muiitem"] = ModernItem.objects.filter(modern__in=context["modernui"])
                #contexthtml1 += Template('{% extends "base/blocks/modern.html" %}').render(context)
            if temp1 or temp2 or temp3:
                print("sum-2")
                context["htmlblock"] = contexthtml1
                contenthtml0 += Template('{% extends "base/blocks/test2.html" %}').render(context)
                print('itog:')
                print(Template('{% extends "base/blocks/test2.html" %}').render(context))
    result["html"] = contenthtml0
    return result

def viewpage(namePage):
    np = namePage
    if np is None or np == '':
        np = 'home'
    context = Context()
    result = dict()
    result["glob"] = context["pos"] = color_profile.objects.first()
    context["aiupages"] = result["aiupages"] = Pages.objects.all().filter(slug=np)
    if not(context["aiupages"]):
        context["aiupages"] = result["aiupages"] = Pages.objects.filter(slug='404')
    result["html"] = Template('{% extends "base/assets/test2.html" %}').render(context)
    return result