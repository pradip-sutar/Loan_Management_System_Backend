import os
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

ALLOWED_HOSTS = ['*','crmlitebackend.vichaarlab.in']


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

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- DB paths ---
local_db_path = os.path.join(BASE_DIR, "db.sqlite3")

onedrive_base = os.path.expanduser("~/OneDrive")
onedrive_db_folder = os.path.join(onedrive_base, "Database")
onedrive_db_path = os.path.join(onedrive_db_folder, "db.sqlite3")

# Logic: If OneDrive exists
if os.path.exists(onedrive_base):
    os.makedirs(onedrive_db_folder, exist_ok=True)

    if os.path.exists(local_db_path) and not os.path.exists(onedrive_db_path):
        # Case: OneDrive newly added, copy existing local DB
        try:
            shutil.copy2(local_db_path, onedrive_db_path)
            print("Copied local DB to OneDrive.")
        except Exception as e:
            print(f"Failed to copy DB to OneDrive: {e}")
    
    # Use OneDrive DB
    db_path = onedrive_db_path
else:
    # Fallback: use local DB
    db_path = local_db_path

# Django DATABASES setting
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': db_path,
        'OPTIONS': {
            'timeout': 40,
        }
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


# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',  # Add this line
#     ),
#     # 'DEFAULT_PERMISSION_CLASSES': (
#     #     'rest_framework.permissions.IsAuthenticated',  # All views will require authentication by default
#     # ),
# }

from datetime import timedelta

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # or however long you want
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
#     'ROTATE_REFRESH_TOKENS': True,
#     'BLACKLIST_AFTER_ROTATION': True,

#     'AUTH_HEADER_TYPES': ('Bearer',),
#     'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
# }

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

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
    # Add other trusted origins if necessary
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


CORS_ORIGIN_ALLOW_ALL = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

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



# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'SCOPE': [
#             'profile',
#             'email',
#         ],
#         'AUTH_PARAMS': {
#             'access_type': 'online',
#         }
#     }
# }


# Celery Settings
# CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Using Redis as the message broker
# CELERY_ACCEPT_CONTENT = ['json']  # Accept only JSON format
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_TASK_IGNORE_RESULT = True
# Celery Result Backend
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# CELERY_TIMEZONE = 'Asia/Kolkata'

# CELERY_BEAT_SCHEDULE = {
#     'generate_demand': {
#         'task': 'sales.tasks.generate_demand',
#         'schedule': crontab(hour=0,minute=0),  # Runs every night at 11:30 PM
#     },
#     'send_demand_reminders': {
#         'task': 'sales.tasks.send_demand_reminders',
#         'schedule': crontab(hour=0,minute=15),  # Runs every night at 11:45 PM
#     },
#     'apply_penalty_daily': {
#         'task': 'sales.tasks.apply_penalties_task',
#         'schedule': crontab(hour=0,minute=30),  # Runs every night at 12:30 AM (midnight)
#     },
# }


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static/')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'dist', 'assets'),  # or 'static' depending on your React config
# ]
MEDIA_URL = 'api/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,MEDIA_URL)

# STORAGES = {
#     "default": {
#         "BACKEND": "storages.backends.s3.S3Storage",
#         "OPTIONS": {
#             "access_key": os.getenv("AMAZON_S3_ACCESS"),
#             "secret_key": os.getenv("AMAZON_S3_SECRET"),
#             "bucket_name": os.getenv("AMAZON_S3_BUCKET"),
#             "region_name": os.getenv("AMAZON_S3_REGION"),
#             "file_overwrite": True,
#             # "default_acl": "public-read",
#             "signature_version": "s3v4",
#         },
#     },
#     "staticfiles": {
#         "BACKEND": "storages.backends.s3.S3Storage",
#         "OPTIONS": {
#             "access_key": os.getenv("AMAZON_S3_ACCESS"),
#             "secret_key": os.getenv("AMAZON_S3_SECRET"),
#             "bucket_name": os.getenv("AMAZON_S3_BUCKET"),
#             "region_name": os.getenv("AMAZON_S3_REGION"),
#             "file_overwrite": True,
#             # "default_acl": "public-read",
#             "signature_version": "s3v4",
#         },
#     },
# }

# STATIC_URL = 'https://propvichaarcrm.s3.amazonaws.com/staticfiles/'
# STATIC_ROOT = 'staticfiles'

# MEDIA_URL = 'https://propvichaarcrm.s3.amazonaws.com/media/'
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {message}',
#             'style': '{',
#         },
#         'simple': {
#             'format': '{levelname} {message}',
#             'style': '{',
#         },
#     },
#     'filters': {
#         'user_context': {
#             '()': 'django.utils.log.CallbackFilter',
#             'callback': lambda record: True,  # To pass user context to the logger
#         },
#     },
#     'handlers': {
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR, 'syslogs.log'),
#             'formatter': 'verbose',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#     },
# }
