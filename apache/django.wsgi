import os
import sys
 
path = '/home/user'
if path not in sys.path:
    sys.path.insert(0, '/home/user')
 
os.environ['DJANGO_SETTINGS_MODULE'] = 'xcms.settings'
 
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
