import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'local-development-only-examenfinal')
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']
INSTALLED_APPS = ['rest_framework', 'vehiculos']
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware', 'django.middleware.common.CommonMiddleware']
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
DATABASES = {'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': os.getenv('DB_NAME', 'examenfinal_vehiculos'),
    'USER': os.getenv('DB_USER', 'root'),
    'PASSWORD': os.getenv('DB_PASSWORD', ''),
    'HOST': os.getenv('DB_HOST', '127.0.0.1'),
    'PORT': os.getenv('DB_PORT', '3306'),
    'OPTIONS': {'charset': 'utf8mb4', 'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
}}
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'UNAUTHENTICATED_USER': None,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Guatemala'
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
