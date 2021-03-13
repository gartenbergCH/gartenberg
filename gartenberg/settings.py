"""
Django settings for gartenberg project.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get('JUNTAGRICO_SECRET_KEY')
DEBUG = os.environ.get("JUNTAGRICO_DEBUG", 'True') == 'True'

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
            ],
            'debug': True
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

DATE_INPUT_FORMATS = ['%d.%m.%Y',]

AUTHENTICATION_BACKENDS = (
    'juntagrico.util.auth.AuthenticateWithEmail',
    'django.contrib.auth.backends.ModelBackend'
)


MIDDLEWARE = [
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

WHITELIST_EMAILS = []


def whitelist_email_from_env(var_env_name):
    email = os.environ.get(var_env_name)
    if email:
        WHITELIST_EMAILS.append(email.replace('@gmail.com', '(\+\S+)?@gmail.com'))


if DEBUG is True:
    for key in os.environ.keys():
        if key.startswith("JUNTAGRICO_EMAIL_WHITELISTED"):
            whitelist_email_from_env(key)


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
ORGANISATION_ADDRESS = {"name":"Gartenberg", 
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
    'welcome': 'gartenberg_emails/member/member_welcome.txt',
    'co_welcome': 'gartenberg_emails/member/co_member_welcome.txt',
    's_created': 'gartenberg_emails/member/share_created.txt',
}
