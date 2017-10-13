from clonecademy.settings import *
import settings_secret as secrets

# ADMIN Settings
# These settings can and need to be changed for production.
ADMINS = (
    (secrets.ADMIN_NAME, secrets.ADMIN_EMAIL),
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'mail.d120.de'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'cvoelcker'
EMAIL_HOST_PASSWORD = secrets.EMAIL_HOST_PASSWORD

DEFAULT_FROM_EMAIL = "{}, {}".format(secrets.ADMIN_NAME, secrets.ADMIN_EMAIL)
SERVER_EMAIL = DEFAULT_FROM_EMAIL


# Production settings
# Only touch if you know what your doing

DEBUG = True

ALLOWED_HOSTS = ['*']

SECRET_KEY = secrets.SECRET_KEY

MANAGERS = ADMINS
EMAIL_SUBJECT_PREFIX = ''

URL_PREFIX = 'api/'
SESSION_COOKIE_SECURE = True

# @see https://docs.djangoproject.com/es/1.9/topics/email/

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'de-DE'

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
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'auth': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}
