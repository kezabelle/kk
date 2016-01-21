# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import sys
from django.conf import settings

DEBUG = os.environ.get('DEBUG', 'on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY', 'TESTTESTTESTTESTTESTTESTTESTTEST')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,testserver').split(',')
BASE_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
    INSTALLED_APPS=(
        'django.contrib.staticfiles',  # better runserver
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'django.contrib.sitemaps',
        'django.contrib.auth',
        'django.contrib.admin',
        'varlet.apps.PageAppConfig',
    ),
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    STATIC_ROOT=os.path.join(BASE_DIR, '__static__'),
    MEDIA_ROOT=os.path.join(BASE_DIR, '__uploads__'),
    STATIC_URL='/__static__/',
    MEDIA_URL='/__uploads__/',
    MESSAGE_STORAGE='django.contrib.messages.storage.cookie.CookieStorage',
    SESSION_ENGINE='django.contrib.sessions.backends.signed_cookies',
    SESSION_COOKIE_HTTPONLY=True,
    SITE_ID=1,
    TEMPLATE_DISPLAY_NAMES={},
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                os.path.join(BASE_DIR, 'templates')
            ],
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
)



def lazy_urls():
    from django.conf.urls import url, include
    from django.contrib import admin
    try:
        from fastsitemaps.views import sitemap
    except ImportError:
        from django.contrib.sitemaps.views import sitemap
    from varlet import named_urls as varlet_urls
    from varlet.sitemaps import PageSitemap
    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^sitemap.xml$', sitemap, {'sitemaps': {'pages': PageSitemap()}}, name='xml_sitemap'),
        url(r'^', include(varlet_urls)),
    ]
    return urlpatterns
from django.utils.functional import SimpleLazyObject
urlpatterns = SimpleLazyObject(lazy_urls)



from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)