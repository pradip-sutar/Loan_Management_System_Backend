import os, sys
from pathlib import Path
# from celery.schedules import crontab
from dotenv import load_dotenv
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s2t15la3dmjleevit5nb7$6ow5tk538#&be4#ac^6j0mjh81!7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*','crmlitebackend.vichaarlab.in','https://lvwjxl9l-8001.inc1.devtunnels.ms',
]

# Application definition

INSTALLED_APPS = [
    # 'daphne',  # ASGI WebSocket Server
    # 'channels',  # Django Channels
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Django REST Framework Token Authentication
    'rest_framework',
    'rest_framework.authtoken',
    # 'rest_framework_simplejwt.token_blacklist',

    # 'django_celery_beat',
    'corsheaders',

    # Project Application
    # 'Dashboard',
    'System_Admin',
    'Employee_Management',
    'Authentication',
]


# Channel Layers 
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",  
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Loan_Management_System_Backend.urls'

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

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

WSGI_APPLICATION = 'Loan_Management_System_Backend.wsgi.application'
# ASGI application
# ASGI_APPLICATION = 'Loan_Management_System_Backend.asgi.application'

DJREST_AUTH_TOKEN_MODEL = None

import os
import shutil

# Flag to reset DB dynamically
force_reset = os.getenv('RESET_DB', 'false').lower() == 'true'
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if getattr(sys, 'frozen', False):
    app_data_dir = Path(os.getenv('APPDATA')) / 'Loan_Management_System_Backend'
    app_data_dir.mkdir(parents=True, exist_ok=True)
    db_path = app_data_dir / 'db.sqlite3'

    # Reset DB if flag is set or if DB is missing or empty  
    if force_reset or not db_path.exists() or os.path.getsize(db_path) == 0:
        try:
            if db_path.exists():
                db_path.unlink()  # Delete existing DB
            bundled_template = Path(sys._MEIPASS) / 'template_db' / 'db.sqlite3'
            shutil.copy(bundled_template, db_path)
        except Exception as e:
            raise RuntimeError(f"Failed to copy bundled DB: {e}")

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': db_path,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }



# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "crmlite_prod",
#         "USER": "vichaarlab",
#         "PASSWORD": "vichaar@2025",
#         "HOST": "147.93.103.104",
#         "PORT": "5432",
#     }
# }

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

from datetime import timedelta


DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000000

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'  # Replace with your server's time zone
USE_TZ = True

USE_I18N = True

USE_TZ = True

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:8000',
    'https://crmlitebackend.vichaarlab.in',
    'http://dialurban.net',
    'http://localhost:5173',
    'http://localhost:8001'
    # Add other trusted origins if necessary
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


CORS_ORIGIN_ALLOW_ALL = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://crmlitebackend.vichaarlab.in',
    'http://dialurban.net',
    ]

AUTH_USER_MODEL = 'Authentication.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # default
    # 'allauth.account.auth_backends.AuthenticationBackend',
]

ADMIN_HOSTED_URL = os.getenv('ADMIN_HOSTED_URL')


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # collectstatic will put files here

MEDIA_URL = 'api/media/'
if getattr(sys, 'frozen', False):
    app_data_dir = Path(os.getenv('APPDATA')) / 'Loan_Management_System_Backend'
    app_data_dir.mkdir(parents=True, exist_ok=True)
    MEDIA_ROOT = app_data_dir / 'media'
else:
    MEDIA_ROOT = BASE_DIR / 'media'

MEDIA_URL = '/api/media/'
