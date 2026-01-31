
import os
import django
from django.conf import settings
from django.template import Template, Context, Engine

# Configure minimal settings
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'parler',
            'main',
        ],
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.abspath('.')], 
            'APP_DIRS': True,
        }],
        USE_I18N=True,
        SECRET_KEY='dummy',
        INSTALLED_APPS_BUG_FIX='main', 
    )
    django.setup()

from django.template.loader import get_template

try:
    print("Attempting to load template...")
    # We load the file directly to see if it parses
    template = get_template('main/templates/main/home.html')
    print("Template loaded successfully.")
except Exception as e:
    print(f"Caught exception: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
