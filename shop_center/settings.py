
from pathlib import Path
import os

from ckeditor_demo.settings import CKEDITOR_UPLOAD_PATH, CKEDITOR_ALLOW_NONIMAGE_FILES, CKEDITOR_CONFIGS

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(q3%xki!t%gbff43ex)=a+hoaaqmm1z5^$op$_!=ymv*de0_kv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.main.apps.MainConfig',
    'apps.accounts.apps.AccountsConfig',
    'apps.products.apps.ProductsConfig',
    'apps.orders.apps.OrdersConfig',
    'apps.discounts.apps.DiscountsConfig',
    'apps.payments.apps.PaymentsConfig',
    'apps.warehouses.apps.WarehousesConfig',
    'apps.comment_scoring_favorites.apps.CommentScoringFavoritesConfig',
    'django_admin_listfilter_dropdown',
    'ckeditor',
    'ckeditor_uploader',
    'django_render_partial',
    'django.contrib.humanize',
    'django_filters',
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

ROOT_URLCONF = 'shop_center.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR / 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.main.views.media_admin'
            ],
        },
    },
]

WSGI_APPLICATION = 'shop_center.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shop_center',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static/'),]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.CustomUser'

CKEDITOR_UPLOAD_PATH='images/ckeditor/upload_files/'
CKEDITOR_ALLOW_NONIMAGE_FILES= False
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Link', 'Unlink', 'Image',],
        ],
    },
    'special':
        {
            'toolbar': 'Special','height': 500,
            'toolbar':'full',
            'toolbar_special':
                [
                    ['Bold'],
                    ['CodeSnippet'],
                ], 'extraPlugins':','.join(['codesnippet','clipboard']),
        },
    'special_an':
        {
            'toolbar': 'Special','height': 500,
            'toolbar_Special':
                [
                    ['Bold'],
                    ['CodeSnippet'],
                ], 'extraPlugins': ','.join(['codesnippet',]),
        },
    'special_an':
        {
            'toolbar': 'Special','height': 500,
            'toolbar_Special':
            [
                ['Bold'],
                ['CodeSnippet'],
            ], 'extraPlugins': ','.join(['codesnippet',]),
        }
}