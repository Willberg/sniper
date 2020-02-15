"""
Django settings for sniper project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import requests
from mongoengine import connect

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y3hfyql)dl5q^o8q+1zeepdzp^h+&2=3r%fd083*y@u)%n0*rb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'oss',
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

ROOT_URLCONF = 'sniper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'sniper.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# 设置全局认证
# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": ['sniper.utils.auth.Authentication', ],  # 里面写你的认证的类的路径
#     "DEFAULT_PERMISSION_CLASSES": ['sniper.utils.permission.SVIPPermission', ],  # 全局配置
# }

# 从服务发现中心获取各项服务
DROWRANGER_NAME = "drowranger_0001"
DROWRANGER_SECRET = "90cea09b4cf234a146a232a8e356e507"
DROWRANGER_SERVICE_URL = "http://127.0.0.1:10000/api/services/v1/list"
headers = {
    "service": DROWRANGER_NAME,
    "secret": DROWRANGER_SECRET
}
DROWRANGER_SERVICE_DICTS = requests.get(DROWRANGER_SERVICE_URL, headers=headers).json()['data']

# SESSION服务
SESSION_SERVICE_NAME = 'am_0001'
SESSION_COOKIE_NAME = "dsessionid"
SESSION_SERVICE = DROWRANGER_SERVICE_DICTS[SESSION_SERVICE_NAME]

# sniper服务
SNIPER_NAME = 'sniper_0001'
SNIPER_SERVICE = DROWRANGER_SERVICE_DICTS[SNIPER_NAME]

# mongo 设置
MONGO_DB_NAME = 'sniper'
MONGO_HOST = '192.168.0.105'
MONGO_PORT = 27017
MONGO_USER_NAME = 'root'
MONGO_PASSWORD = '123456'
connect(db=MONGO_DB_NAME, host=MONGO_HOST, port=MONGO_PORT, username=MONGO_USER_NAME, password=MONGO_PASSWORD,
        authentication_source='admin')

# redis在django中的配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.0.105:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # 压缩支持
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            # 配置默认连接池
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            # json 序列化,默认是使用pickle直接将对象存入redis,改用json
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
            "PASSWORD": "test123",
        }
    }
}
