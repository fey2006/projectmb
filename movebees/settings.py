"""
Django settings for movebees project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!s!no#0f0u)-rd9!rqsd$pextk*n#ec80(lbkp8j*%hs4!+052'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = (
    'templates/',
)

ACCOUNT_ACTIVATION_DAYS = 2
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'testing@example.com'

LOGIN_REDIRECT_URL = '/'

# Application definition

GOOGLE_SECRET_KEY = 'AIzaSyAe50PasAkJ_JS4hJZfFnrIKqqmprjp1Lc'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.gis',
    'shop',
    'registration',
    #'django_comments',
    'rest_framework',
    'rest_framework.authtoken',
)

COMMENTS_APP = 'shop'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'movebees.urls'

WSGI_APPLICATION = 'movebees.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME': 'movebees_db',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME': 'ivanyat2013$movebees_db',
        'USER': 'ivanyat2013',
        'PASSWORD': '123456',
        'HOST': 'mysql.server',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}
'''

#GEOS_LIBRARY_PATH = r'C:\OSGeo4W64\bin\geos_c.dll'
#GDAL_LIBRARY_PATH = r'C:\OSGeo4W64\bin\gdal115.dll'
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'ivanyat2013@gmail.com '
EMAIL_HOST_PASSWORD = '2WrsBTjN9G144YFN4HIHCA'

AUTH_PROFILE_MODULE = "shop.RegistrationProfile"

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework.authentication.SessionAuthentication',
         ),
 }

#REST_REGISTRATION_BACKEND = rest_auth.backends.rest_registration.RESTRegistrationView'
REST_REGISTRATION_BACKEND = 'registration.backends.default.views.RegistrationView'
REST_PROFILE_MODULE = 'shop.UserProfile'

REGISTRATION_API_ACTIVATION_SUCCESS_URL = '/registration/activation_complete.html'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT =  os.path.realpath(os.path.dirname(__file__))+'/../images/'
STATIC_ROOT = os.path.realpath(os.path.dirname(__file__))+'/../'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"



STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)