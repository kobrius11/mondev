"""
Django settings for mondev project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from . import local_settings


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = local_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'mondev_site',
    'user_profile',
    'academy',
    'tinymce',
    'adminsortable2',
    'rest_framework',
    'rest_framework.authtoken',    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'verify_email',
    'monda_base',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'monda.urls'

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

WSGI_APPLICATION = 'monda.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # },
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'postgres',
        'NAME': local_settings.POSTGRES_DB,
        'USER': local_settings.POSTGRES_USER,
        'PASSWORD': local_settings.POSTGRES_PASSWORD,
        'PORT': local_settings.POSTGRES_PORT,
    }
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

LANGUAGES = (
    (LANGUAGE_CODE, 'English'),
    ('lt', 'Lietuvių'),
)

TIME_ZONE = 'Europe/Vilnius'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR.joinpath(STATIC_URL)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR.joinpath(MEDIA_URL)


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = '/'

INTERNAL_IPS = [
    "127.0.0.1",
]

TINYMCE_DEFAULT_CONFIG = {
    'height': 300,
    'cleanup_on_startup': False,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'plugins': 'contextmenu textcolor lists directionality visualchars charmap media image advlist autolink code',
    'toolbar1': '''
            code removeformat | formatselect bold italic underline forecolor backcolor | 
            alignleft alignright aligncenter alignjustify | indent outdent bullist numlist |
            visualblocks visualchars | charmap | image media
            ''',
    'statusbar': True,
    'menubar': False,
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# Email config
# https://pypi.org/project/Django-Verify-Email/

SUBJECT = 'Welcome to Middle of Nowhere!'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = local_settings.EMAIL_ID
EMAIL_HOST_PASSWORD = local_settings.EMAIL_PW
DEFAULT_FROM_EMAIL = local_settings.DEFAULT_FROM_EMAIL # no_reply@MoNDA.live
LOGIN_URL = 'login'
EXPIRE_AFTER = '2m' # email expires after 2 minutes, MAX_RETRIES = 2(default)

VERIFICATION_SUCCESS_MSG = """Your Email is verified successfully and account has been activated.
You can login with the credentials now..."""


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # File handler for logging DEBUG and above messages to 'django_error.log', 'app.log' and 'console' files.
    "handlers": {
        "file_for_django": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "logs/django_error.log",
        },
        "file_for_apps": {
            "level": "DEBUG",
            "class": "logging.FileHandler", 
            "filename": "logs/app.log",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    # Django logger configuration: log WARNING, INFO and above messages to 'django_error.log' and app.log.
    "loggers": {
        "django": {
            "handlers": ["file_for_django"],
            "level": "WARNING",
            "propagate": True,
        },
        "user_profile": {  
            "handlers": ["file_for_apps"],
            "level": "INFO",  
            "propagate": False,
        },
    },
}

# If DEBUG is True, add the console handler to all logger configurations.
if DEBUG:
    for logger_config in LOGGING["loggers"].values():
        if "console" not in logger_config["handlers"]:
            logger_config["handlers"].append("console")
