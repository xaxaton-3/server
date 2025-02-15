import os
import pathlib

from dotenv import load_dotenv


load_dotenv()


def get_bool_from_env(name: 'str|None', default: bool) -> bool:
    env_variable = os.environ.get(name)
    if env_variable is None:
        return default
    return env_variable.lower() in {'true', '1', 'yes', 'on'}


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

USE_LITE_DB = get_bool_from_env('USE_LITE_DB', False)

SECRET_KEY = os.environ.get('SECRET_KEY', 'no-so-secret')
DEBUG = get_bool_from_env('DEBUG', True)
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split()
MISTRAL_TOKEN = os.environ.get('MISTRAL_TOKEN')
MAX_PERSON_HISTORY_LENGTH = 1000

POSTGRES_HOST = os.environ.get('POSTGRES_HOST', default='db')
POSTGRES_DB = os.environ.get('POSTGRES_DB', default='fatherland_defender')
POSTGRES_USER = os.environ.get('POSTGRES_USER', default='postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', default='12345')

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'activity_journal.apps.ActivityJournalConfig',
    'ai_helper.apps.AiHelperConfig',
    'content.apps.ContentConfig',
    'notification.apps.NotificationConfig',
    'users.apps.UsersConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'fatherland_defender.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'fatherland_defender.wsgi.application'

SQLITE_CONFIG = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3'
    }

POSTGRES_CONFIG = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': POSTGRES_DB,
    'HOST': POSTGRES_HOST,
    'USER': POSTGRES_USER,
    'PASSWORD': POSTGRES_PASSWORD,
    'PORT': '5432',
}

MAIN_DB = POSTGRES_CONFIG if not USE_LITE_DB else SQLITE_CONFIG

DATABASES = {
    'default': MAIN_DB,
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

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/assets/'
STATICFILES_DIRS = [BASE_DIR / 'assets']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default_formatter': {
            'format': '{levelname} {asctime} {function} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
    },
    'loggers': {
        'fdef_logger': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

try:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False
    EMAIL_PORT = 587
    EMAIL_HOST_USER = os.environ['EMAIL_SENDER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASSWORD']
except KeyError:
    EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
