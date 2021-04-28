import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DevelopsTodayTask.settings')

application = get_wsgi_application()
