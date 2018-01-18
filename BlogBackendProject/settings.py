"""
Django settings for BlogBackendProject project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys

from .private import DATABASE_CONFIG, EMAIL_CONFIG, PRIVATE_QINIU_ACCESS_KEY, PRIVATE_QINIU_SECRET_KEY, \
    PRIVATE_QINIU_BUCKET_DOMAIN, PRIVATE_QINIU_BUCKET_NAME, PRIVATE_QINIU_GET_OBJECT_BASE_URL

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#vam9e79q3!tq8pje@19!3z8c#seafwogk)%i8)e$83nmftgfg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'user.UserProfile'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PERSONAL_APPS = [
    'index',
    'base.apps.BaseConfig',
    'material.apps.MaterialConfig',
    'movie.apps.MovieConfig',
    'album.apps.AlbumConfig',
    'article.apps.ArticleConfig',
    'user.apps.UserConfig',
    'user_operation.apps.UserOperationConfig'
]

EXTRA_APPS = [
    'xadmin',
    'DjangoUeditor',
    'django_filters',
    'crispy_forms',
    'pagedown',
    'rest_framework',
    'corsheaders'
]

INSTALLED_APPS += PERSONAL_APPS + EXTRA_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 必须跟原域匹配才可获取发送 cookie 的权限
CORS_ORIGIN_REGEX_WHITELIST = r'.*'
# 必须有这个才接受前端跨域发送 cookie
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'BlogBackendProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'BlogBackendProject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': DATABASE_CONFIG
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_URL = PRIVATE_QINIU_GET_OBJECT_BASE_URL
MEDIA_ROOT = ''

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication', # 会引起前台Ajax出现跨域无法访问的问题
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100000/day',
        'user': '100000/day'
    },
    'UPLOADED_FILES_USE_URL': True
}

# email setting
EMAIL_HOST = EMAIL_CONFIG['EMAIL_HOST']
EMAIL_PORT = EMAIL_CONFIG['EMAIL_PORT']
EMAIL_HOST_USER = EMAIL_CONFIG['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = EMAIL_CONFIG['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = EMAIL_CONFIG['EMAIL_USE_TLS']
EMAIL_FROM = EMAIL_CONFIG['EMAIL_FROM']

# QINIU

QINIU_ACCESS_KEY = PRIVATE_QINIU_ACCESS_KEY
QINIU_SECRET_KEY = PRIVATE_QINIU_SECRET_KEY
QINIU_BUCKET_NAME = PRIVATE_QINIU_BUCKET_NAME['post']
QINIU_BUCKET_DOMAIN = PRIVATE_QINIU_BUCKET_DOMAIN
QINIU_SECURE_URL = False

DEFAULT_FILE_STORAGE = 'qiniustorage.backends.QiniuMediaStorage'
