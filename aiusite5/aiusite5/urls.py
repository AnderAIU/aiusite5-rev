"""
URL configuration for aiusite5 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.contrib.sitemaps.views import sitemap
from .sitemaps import *

from django.conf.urls.static import static
from django.conf import settings

from aiusite5.views import page_index, pageNotFound
from aiupages.views import *
from aiucolors.views import css_renderer, js_renderer
from convertpdf.views import *
from .views import pagesroute, robots_txt

from django.views.generic import TemplateView

handler404 = pageNotFound

sitemaps = {
    'dynamic': DynamicViewSitemap,
}

urlpatterns = [
    path('', PageView.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path('get_pages/', get_pages, name='get_pages'),
    path('get_files/', get_files, name='get_param'),
    path('css/<str:filename>.css', css_renderer),
    path('js-<str:slug>/<str:filename>.js', js_renderer),
    path('get_param/', get_param, name='get_param'),
    path('doc/', openfile, name="openfile"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt),
    path('lk/', include('django.contrib.auth.urls')),
    path('<str:extpages>/', pagesroute),
]

if settings.DEBUG:
    if settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    if settings.STATIC_ROOT:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)