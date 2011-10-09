# coding=utf-8
# Django settings for deployment on ep.io

from settings import *

DEBUG = False
TEMPLATE_DEBUG = False

INSTALLED_APPS = (
    # Contrib apps
    'django.contrib.staticfiles',
    # Own apps
    'apps.front',
)
