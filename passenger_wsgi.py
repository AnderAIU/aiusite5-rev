# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/home/a/anderhul/anderaiu.su/aiusite5')
#sys.path.insert(1, '/home/a/anderhul/.local/lib/python3.11/site-packages')
sys.path.insert(1, '/home/a/anderhul/.local/lib/python3.11/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'aiusite5.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()