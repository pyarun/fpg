"""
Django settings for nlms project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from django.core.exceptions import ImproperlyConfigured

"""
Django settings for organic project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

DJANGO_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
BASE_DIR = os.path.abspath(os.path.dirname(DJANGO_DIR))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "40ipur$+7j=s)i$(f9-mo6ed60s2luvx$)3&oyjq!t*5@)%g(!"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'django_extensions',
    'django_js_reverse',
    'debug_toolbar',
    'registration',
    'rest_framework',
    'photologue',
    'sortedm2m',

    'profiles',
    'utils',
    'address',
    'facility',


)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'fpg.urls'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "asset")
# Additional locations of static files
STATICFILES_DIRS = (
    os.path.abspath(os.path.join(DJANGO_DIR, "static")),
)

SITE_ID = 1

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.static',

    'django.contrib.messages.context_processors.messages',

)

# adding languages for django-cms
LANGUAGES = [
    ('en-us', 'English'),
]

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(DJANGO_DIR, "templates"),
    # os.path.join(PROJECT_PATH, "templates", "cms", "plugins"),
)

MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, "media"))

MEDIA_URL = "/media/"

AUTHENTICATION_BACKENDS = (
    'fpg.emailauthbackend.EmailAuthBackend',
)

ANONYMOUS_USER_ID = None

FIXTURE_DIRS = (os.path.abspath(os.path.join(DJANGO_DIR, "fixtures")),)


# ######## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            # 'class': 'nlms.logger.ColorizingStreamHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'fpg': {
            'handlers': ['console', 'mail_admins'],
            'level': 'DEBUG'
        }
    }
}
# ######### END LOGGING CONFIGURATION


# ######### MANAGER CONFIGURATION
# developers are requested to copy below settings in their own settings and modified as required.
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Arun', 'arun@vertisinfotech.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = (
    ('Arun', 'arun@vertisinfotech.com'),
)
# ######### END MANAGER CONFIGURATION

INTERNAL_IPS = ("127.0.0.1",)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

ACCOUNT_ACTIVATION_DAYS = 7  # One-week activation window; you may, of course, use a different value.

LOGIN_REDIRECT_URL = '/'

AUTH_USER_MODEL = 'auth.User'


try:
    from local_settings import *
except:
    ImproperlyConfigured("local settings file is not configured for this server.")
