from django.contrib import sitemaps
from django.urls import reverse
from aiupages.models import *

class DynamicViewSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return Pages.objects.all()

    def location(self, item):
        return f'/{item.slug}'