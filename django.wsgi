import os
import sys
(head, tail) = os.path.split(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(head)
sys.path.append(os.path.join(head,tail))
sys.path.append(os.path.join(head,tail, 'pylib'))


os.environ['DJANGO_SETTINGS_MODULE'] = 'cacerp.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

