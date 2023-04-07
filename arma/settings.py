# from pathlib import Path
# import os
# import dj_database_url
# from dotenv import load_dotenv
# load_dotenv()
#
# IS_PRODUCTION = False
#
# DEBUG = False
#
#  # Get the current working
# cwd = os.getcwd()
# print("Current working directory:", cwd)
#
# if os.getcwd() == "/app":
#     DEBUG = False
#     IS_PRODUCTION = True
#
# # DATABASES['default'] = dj_database_url.parse('postgres://username:password@example.com:5432/database')
# # DATABASES['default'] = dj_database_url.config()
# # DATABASES['default'] = dj_database_url.config('postgres://username:password@example.com:5432/database')
#  # DATABASES = ['default'].update(db_from_env)
#
# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
#
# # DATABASE_URL = os.environ['DATABASE_URL']
# DATABASE_URL = 'postgres://tubphmzekpfhbv:d901cee21a961066447a15323a0555af25cb008f35eb69b762d64c853c979e47@ec2-176-34-211-0.eu-west-1.compute.amazonaws.com:5432/djjlihih2flh9'
#
# db_from_env = dj_database_url.config(conn_max_age=600)
#
# # Quick-start development settings - unsuitable for production
# # See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/
#
# ALLOWED_HOSTS = ['armatournaments.herokuapp.com', '127.0.0.1']
# # ALLOWED_HOSTS = os.environ.get(ALLOWED_HOSTS)
# # ALLOWED_HOSTS = ['arma.com']
#
# INSTALLED_APPS = [
#     'dal',
#     'dal_select2',
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'django_extensions',
#     'import_export',
#     'crispy_forms',
#     'sorl.thumbnail',
#     # 'whitenoise.runserver_nostatic',
#     'cloudinary_storage',
#     'cloudinary',
#     #arma:
#     'tournaments.apps.TournamentsConfig',
#     'posts.apps.PostsConfig',
#     'register.apps.RegisterConfig',
#     'organizers.apps.OrganizersConfig',
#     'tournament_calculating.apps.TournamentCalculatingConfig',
#     'galleries.apps.GalleriesConfig',
#     'finals.apps.FinalsConfig',
#     'main.apps.MainConfig',
# ]
#
# CRISPY_TEMPLATE_PACK = 'bootstrap4'
#
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'django_cprofile_middleware.middleware.ProfilerMiddleware',
# ]
#
# DJANGO_CPROFILE_MIDDLEWARE_REQUIRE_STAFF = False
#
# ROOT_URLCONF = 'arma.urls'
#
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR / 'templates'],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#                 'django.template.context_processors.media'
#             ],
#         },
#     },
# ]
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#
#     }
# }
#
# WSGI_APPLICATION = 'arma.wsgi.application'
#
# # Database
# # https://docs.djangoproject.com/en/4.0/ref/settings/#databases
# # Password validation
# # https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
#
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]
#
# # Internationalization
# # https://docs.djangoproject.com/en/4.0/topics/i18n/
#
# LANGUAGE_CODE = 'pl-Pl'
#
# TIME_ZONE = 'UTC'
#
# USE_I18N = True
#
# USE_TZ = True
#
# # Static files (CSS, JavaScript, Images)
# # https://docs.djangoproject.com/en/4.0/howto/static-files/
# STATIC_URL = 'static/'
# if DEBUG:
#     STATICFILES_DIRS = [
#         os.path.join(BASE_DIR, 'static')
#     ]
# else:
#     STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#
# # STATIC_ROOT =  BASE_DIR / "static"
# # STATICFILES_DIRS = [
# #     # BASE_DIR / 'static'
# #     os.path.join(BASE_DIR, 'static'),
# # ]
# # STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')
# # ]
#
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
#
# # MEDIA_ROOT = BASE_DIR / "images"
# MEDIA_ROOT = os.path.join(BASE_DIR, "images")
# MEDIA_URL = "/images/"
#
# # LOCALE_PATHS = [str(BASE_DIR / "locale")]
# # Default primary key field type
# # https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
#
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#
# SHELL_PLUS_PRINT_SQL = True
#
# LOGIN_REDIRECT_URL = "/home"
# LOGOUT_REDIRECT_URL = "/home"
#
# # PYDEVD_USE_CYTHON=NO
# # PYDEVD_USE_FRAME_EVAL=NO
#
# SECRET_KEY = os.getenv('SECRET_KEY')
#
# try:
#     from local_settings import *
# except ImportError:
#     print("no local_settings.py file?")
#
# if IS_PRODUCTION:
#     import dj_database_url
#
#     db_from_env = dj_database_url.config(conn_max_age=500)
#     DATABASES["default"].update(db_from_env)
#
#     SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
#     ALLOWED_HOSTS = ["armatournaments.herokuapp.com"]
#     # debug heroku
#     if DEBUG:
#         import logging
#
#         LOGGING = {
#             "version": 1,
#             "disable_existing_loggers": False,
#             "handlers": {
#                 "console": {
#                     "class": "logging.StreamHandler",
#                 },
#             },
#             "loggers": {
#                 "django": {
#                     "handlers": ["console"],
#                     "level": os.getenv("DJANGO_LOG_LEVEL", "DEBUG"),
#                 },
#             },
#         }
# # else:
#
# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': 'dcgtoiogb',
#     'API_KEY': '327397828378715',
#     'API_SECRET': os.getenv('API_SECRET')
# }
#
# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'





from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv
load_dotenv()

IS_PRODUCTION = True

 # Get the current working
cwd = os.getcwd()
print("Current working directory:", cwd)

# if os.getcwd() == "/app":
#     DEBUG = False
#     IS_PRODUCTION = True

# DATABASES['default'] = dj_database_url.parse('postgres://username:password@example.com:5432/database')
# DATABASES['default'] = dj_database_url.config()
# DATABASES['default'] = dj_database_url.config('postgres://username:password@example.com:5432/database')
 # DATABASES = ['default'].update(db_from_env)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL = 'postgres://tubphmzekpfhbv:d901cee21a961066447a15323a0555af25cb008f35eb69b762d64c853c979e47@ec2-176-34-211-0.eu-west-1.compute.amazonaws.com:5432/djjlihih2flh9'

db_from_env = dj_database_url.config(conn_max_age=600)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

ALLOWED_HOSTS = ['armatournaments.herokuapp.com', '127.0.0.1']
# ALLOWED_HOSTS = os.environ.get(ALLOWED_HOSTS)
# ALLOWED_HOSTS = ['arma.com']

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'import_export',
    'crispy_forms',
    'sorl.thumbnail',
    # 'whitenoise.runserver_nostatic',
    'cloudinary_storage',
    'cloudinary',
    #arma:
    'tournaments.apps.TournamentsConfig',
    'posts.apps.PostsConfig',
    'register.apps.RegisterConfig',
    'organizers.apps.OrganizersConfig',
    'tournament_calculating.apps.TournamentCalculatingConfig',
    'galleries.apps.GalleriesConfig',
    'finals.apps.FinalsConfig',
    'main.apps.MainConfig',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_cprofile_middleware.middleware.ProfilerMiddleware',
]

DJANGO_CPROFILE_MIDDLEWARE_REQUIRE_STAFF = False

ROOT_URLCONF = 'arma.urls'

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
                'django.template.context_processors.media'
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',

    }
}

WSGI_APPLICATION = 'arma.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'pl-Pl'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_URL = 'static/'


# STATIC_ROOT =  BASE_DIR / "static"
# STATICFILES_DIRS = [
#     # BASE_DIR / 'static'
#     os.path.join(BASE_DIR, 'static'),
# ]
# STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')
# ]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# MEDIA_ROOT = BASE_DIR / "images"
MEDIA_ROOT = os.path.join(BASE_DIR, "images")
MEDIA_URL = "/images/"

# LOCALE_PATHS = [str(BASE_DIR / "locale")]
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SHELL_PLUS_PRINT_SQL = True

LOGIN_REDIRECT_URL = "/home"
LOGOUT_REDIRECT_URL = "/home"

# PYDEVD_USE_CYTHON=NO
# PYDEVD_USE_FRAME_EVAL=NO

SECRET_KEY = os.getenv('SECRET_KEY')

try:
    from local_settings import *
except ImportError:
    print("no local_settings.py file?")

if IS_PRODUCTION:
    import dj_database_url

    db_from_env = dj_database_url.config(conn_max_age=500)

    DEBUG = False
    DATABASES["default"].update(db_from_env)
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    ALLOWED_HOSTS = ["armatournaments.herokuapp.com"]
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': 'dcgtoiogb',
        'API_KEY': '327397828378715',
        'API_SECRET': os.getenv('API_SECRET')
    }

    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

    # debug heroku
    if DEBUG:
        import logging

        LOGGING = {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                },
            },
            "loggers": {
                "django": {
                    "handlers": ["console"],
                    "level": os.getenv("DJANGO_LOG_LEVEL", "DEBUG"),
                },
            },
        }

else:

    DEBUG = True
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static')
    ]

