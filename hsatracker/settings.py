import os
from pathlib import Path
import environ

env = environ.Env(DEBUG=(bool, False))
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

INSTALLED_APPS = [
   'django.contrib.admin',
   'django.contrib.auth',
   'django.contrib.contenttypes', 
   'django.contrib.sessions',
   'django.contrib.messages',
   'django.contrib.staticfiles',
   'users',
   'expenses',
]

MIDDLEWARE = [
   'django.middleware.security.SecurityMiddleware',
   'whitenoise.middleware.WhiteNoiseMiddleware',
   'django.contrib.sessions.middleware.SessionMiddleware',
   'django.middleware.common.CommonMiddleware',
   'django.middleware.csrf.CsrfViewMiddleware',
   'django.contrib.auth.middleware.AuthenticationMiddleware',
   'django.contrib.messages.middleware.MessageMiddleware',
   'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hsatracker.urls'

TEMPLATES = [
   {
       'BACKEND': 'django.template.backends.django.DjangoTemplates',
       'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'hsatracker.wsgi.application'
WSGI_MAX_REQUESTS = 1000
WSGI_TIMEOUT = 120

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': env('DATABASE_NAME', default='hsatracker'),
       'USER': env('DATABASE_USER', default='hsatracker_user'),
       'PASSWORD': env('DATABASE_PASSWORD'),
       'HOST': env('DATABASE_HOST', default='db'),
       'PORT': env('DATABASE_PORT', default='5432'),
   }
}

AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'dashboard'

AUTH_PASSWORD_VALIDATORS = [
   {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
   {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    'OPTIONS': {'min_length': 8,}},
   {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
   {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if not DEBUG:
   SECURE_BROWSER_XSS_FILTER = True
   SECURE_CONTENT_TYPE_NOSNIFF = True
   SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   X_FRAME_OPTIONS = 'DENY'
   SECURE_HSTS_SECONDS = 31536000
   SECURE_HSTS_INCLUDE_SUBDOMAINS = True
   SECURE_HSTS_PRELOAD = True

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@hsatracker.org')
EMAIL_SUBJECT_PREFIX = '[HSA Tracker] '  # Prefix for system emails

LOGGING = {
   'version': 1,
   'disable_existing_loggers': False,
   'formatters': {
       'verbose': {
           'format': '[{asctime}] {levelname} {name} {message}',
           'style': '{',
       },
       'simple': {
           'format': '{levelname} {message}',
           'style': '{',
       },
   },
   'handlers': {
       'file_debug': {
           'level': 'DEBUG',
           'class': 'logging.FileHandler',
           'filename': BASE_DIR / 'debug.log',
           'formatter': 'verbose',
       },
       'file_error': {
           'level': 'ERROR',
           'class': 'logging.FileHandler',
           'filename': BASE_DIR / 'error.log',
           'formatter': 'verbose',
       },
       'console': {
           'class': 'logging.StreamHandler',
           'formatter': 'simple',
       },
   },
   'loggers': {
       'django': {
           'handlers': ['file_debug', 'file_error', 'console'],
           'level': env('DJANGO_LOG_LEVEL', default='DEBUG'),
           'propagate': True,
       },
       'gunicorn.error': {
           'level': 'INFO',
           'handlers': ['console'],
           'propagate': True,
       },
       'gunicorn.access': {
           'level': 'INFO',
           'handlers': ['console'],
           'propagate': True,
       },
   },
}