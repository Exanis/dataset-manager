import os
from environ import Env


ENV = Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, 'change me'),
    DATABASE_URL=(str, 'sqlite:////tmp/db.sqlite3'),
    ALLOWED_HOSTS=(list, ['*']),
    LANGUAGE_CODE=(str, 'en-us'),
    TIMEZONE=(str, 'UTC')
)

ENV.read_env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = ENV('SECRET_KEY')
DEBUG = ENV('DEBUG')
ALLOWED_HOSTS = ENV('ALLOWED_HOSTS')
DATABASES = {
    'default': ENV.db()
}
LANGUAGE_CODE = ENV('LANGUAGE_CODE')
TIME_ZONE = ENV('TIMEZONE')

USE_TZ = True

CELERY_APP = 'datama'
CELERY_BROKER_URL = 'amqp://localhost'
CELERY_BIN = 'celery'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'manager'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'datama.urls'

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

WSGI_APPLICATION = 'datama.wsgi.application'
STATIC_URL = '/static/'
STATIC_ROOT = '/dataset-manager-assets/static/'
