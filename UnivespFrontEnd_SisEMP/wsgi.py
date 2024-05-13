"""
WSGI config for UnivespFrontEnd_SisEMP project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os, sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
settings_module = "%s.settings" % PROJECT_ROOT.split(os.sep)[-1]
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UnivespFrontEnd_SisEMP.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
