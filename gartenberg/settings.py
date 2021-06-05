"""
Django settings for gartenberg project.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get('JUNTAGRICO_SECRET_KEY')

DEBUG = os.environ.get("JUNTAGRICO_DEBUG", "False") == "True"

ALLOWED_HOSTS = ['my.gartenberg.ch', 'gartenberg.juntagrico.science', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'juntagrico',
    'impersonate',
    'crispy_forms',
    'adminsorttable2',
    'gartenberg',
]

ROOT_URLCONF = 'gartenberg.urls'

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('JUNTAGRICO_DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('JUNTAGRICO_DATABASE_NAME', 'gartenberg.db'),
        'USER': os.environ.get('JUNTAGRICO_DATABASE_USER'),
        'PASSWORD': os.environ.get('JUNTAGRICO_DATABASE_PASSWORD'),
        'HOST': os.environ.get('JUNTAGRICO_DATABASE_HOST'),
        'PORT': os.environ.get('JUNTAGRICO_DATABASE_PORT', False),
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ]
        },
    },
]

WSGI_APPLICATION = 'gartenberg.wsgi.application'


LANGUAGE_CODE = 'de'
TIME_ZONE = 'Europe/Zurich'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

DATE_INPUT_FORMATS = ['%d.%m.%Y', ]

AUTHENTICATION_BACKENDS = (
    'juntagrico.util.auth.AuthenticateWithEmail',
    'django.contrib.auth.backends.ModelBackend'
)


MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware', # Serve static files
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'impersonate.middleware.ImpersonateMiddleware'
]

EMAIL_HOST = os.environ.get('JUNTAGRICO_EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('JUNTAGRICO_EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('JUNTAGRICO_EMAIL_PASSWORD')
EMAIL_PORT = int(os.environ.get('JUNTAGRICO_EMAIL_PORT', '25'))
EMAIL_USE_TLS = os.environ.get('JUNTAGRICO_EMAIL_TLS', 'False') == 'True'
EMAIL_USE_SSL = os.environ.get('JUNTAGRICO_EMAIL_SSL', 'False') == 'True'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# The white list only applies if the application is executed in debug mode and
# prevents mails from being sent to other adresses
WHITELIST_EMAILS = ['info@gartenberg.ch', 'gartenberg-test@uhlme.ch']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

IMPERSONATE = {
    'REDIRECT_URL': '/my/profile',
}

LOGIN_REDIRECT_URL = "/my/home"

"""
    File & Storage Settings
"""
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

MEDIA_ROOT = 'media'

"""
     Crispy Settings
"""
CRISPY_TEMPLATE_PACK = 'bootstrap4'

"""
     juntagrico Settings
"""
ORGANISATION_NAME = "Gartenberg"
ORGANISATION_LONG_NAME = "Gartenberg"
ORGANISATION_ADDRESS = {"name": "Gartenberg",
                        "street": "Altenberg",
                        "number": "307",
                        "zip": "5063",
                        "city": "Wölflwinswil",
                        "extra": ""}
ORGANISATION_BANK_CONNECTION = {"PC": "",
                                "IBAN": "CH02 8080 8004 4102 8510 0",
                                "BIC": "",
                                "NAME": "Genossenschaft GartenBerg c/o Katharina Maurer, Erlinsbacherstrasse 83, CH-5000 Aarau",
                                "ESR": ""}
SHARE_PRICE = "750"

BUSINESS_REGULATIONS = 'https://gartenbergch.files.wordpress.com/2021/02/betriebsreglement.pdf'
BYLAWS = 'https://gartenbergch.files.wordpress.com/2020/10/gartenberg_statuten.pdf'
FAQ_DOC = 'https://gartenbergch.files.wordpress.com/2020/11/projektbeschrieb-gartenberg-1.pdf'

INFO_EMAIL = "info@gartenberg.ch"
SERVER_URL = "www.gartenberg.ch"
ADMINPORTAL_NAME = "Gartenberg"
ADMINPORTAL_SERVER_URL = "my.gartenberg.ch"
STYLE_SHEET = "/static/gartenberg/css/customize.css"
FAVICON = '/static/gartenberg/img/gartenbergfavicon.ico'

EMAILS = {
    's_created': 'gartenberg_emails/member/share_created.txt',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'gartenberg.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'propagate': True,
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO')
        },
        'juntagrico.mailer': {
            'handlers': ['file', 'console'],
            'propagate': True,
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO')
        },
    },
}

# Needed if you use sqlite to display certain sites
if os.environ.get('JUNTAGRICO_DATABASE_ENGINE', 'django.db.backends.sqlite3') == 'django.db.backends.sqlite3':
    USE_TZ = True