from django.utils import timezone
import os
from dotenv import load_dotenv
import dj_database_url
from pathlib import Path

# Cargar las variables de entorno desde el archivo .env
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')  
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', default='your secret key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = []

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks',
    'storages',  # Agregar esta línea para usar django-storages
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = 'djangocrud.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangocrud.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://postgres:postgres@localhost/postgres',
        conn_max_age=600
    )
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = f'https://{os.getenv("AWS_STORAGE_BUCKET_NAME")}.s3.amazonaws.com/static/'

# This production code might break development mode, so we check whether we're in DEBUG mode
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_DIRS = [
    BASE_DIR / 'tasks/static',
]

# Carpeta para recolectar los archivos estáticos al ejecutar collectstatic
#STATIC_ROOT = BASE_DIR / 'staticfiles'

LOGIN_URL = '/signin'

# Configuración para archivos multimedia
MEDIA_URL = f'https://{os.getenv("AWS_STORAGE_BUCKET_NAME")}.s3.amazonaws.com/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuración para AWS S3
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')  # Debes establecer estas variables de entorno en tu servidor o archivo .env
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'djangocrudprojectred'  # El nombre de tu bucket en S3
AWS_S3_REGION_NAME = 'us-east-1'  # La región del bucket
AWS_S3_SIGNATURE_VERSION = 's3v4'

# Almacenamiento de archivos estáticos en S3 (si quieres también almacenar estáticos en S3)
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# Configurar el backend de almacenamiento de archivos para S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Si usas archivos estáticos en S3, habilita esto también
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Especifica si tu bucket tiene contenido público
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
