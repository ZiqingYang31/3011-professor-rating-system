
import os
import sys

if 'PYTHONANYWHERE_DOMAIN' in os.environ:
    path = '/home/sc22zy/3011-professor-rating-system'
else:
    path = os.path.dirname(os.path.abspath(__file__))

if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'professor_rating.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
