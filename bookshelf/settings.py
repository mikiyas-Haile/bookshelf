from pathlib import Path
import django_heroku
import dj_database_url
import os
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-etc5*r$g@4wchswuuyg^so^$!(b-*ae)j&m$dv$2%zma%$$q7^'

DEBUG = True

ALLOWED_HOSTS = []

BOOK_ACTIONS = ['create', 'like', 'unlike', 'reply']
INSTALLED_APPS = [
     'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'knox',

    'accounts',
    'main',
    'readers',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bookshelf.urls'

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

WSGI_APPLICATION = 'bookshelf.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DISABLE_COLLECTSTATIC = 1
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

STATIC_ROOT = os.path.join(BASE_DIR / 'static-root')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


DEFAULT_RENDERER_CLASSES = [
        'rest_framework.renderers.JSONRenderer',
    ]

DEFAULT_AUTHENTICATION_CLASSES = [
        'rest_framework.authentication.SessionAuthentication',
        'knox.auth.TokenAuthentication',
    
]


if DEBUG:
    # DEFAULT_AUTHENTICATION_CLASSES += [
    #     'zebidar.rest_api.dev.DevAuthentication'
    # ]
    DEFAULT_RENDERER_CLASSES += [
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
REST_FRAMEWORK = {
    
    'DEFAULT_AUTHENTICATION_CLASSES': DEFAULT_AUTHENTICATION_CLASSES,
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES
}
django_heroku.settings(locals())