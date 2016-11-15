# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import sys
from django.conf import settings

DEBUG = os.environ.get('DEBUG', 'on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY', 'TESTTESTTESTTESTTESTTESTTESTTEST')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,testserver,kez').split(',')
BASE_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

if DEBUG:
    DEBUG_APPS = (
        'debug_toolbar.apps.DebugToolbarConfig',
    )
    DEBUG_MIDDLEWARE = (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
else:
    DEBUG_APPS = ()
    DEBUG_MIDDLEWARE = ()

settings.configure(
    DEBUG=DEBUG,
    # have to manually setup djdt because of lazy_urls, see
    # https://code.djangoproject.com/ticket/26287
    DEBUG_TOOLBAR_PATCH_SETTINGS=False,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    INTERNAL_IPS=('127.0.0.1',),
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ) + DEBUG_MIDDLEWARE,
    INSTALLED_APPS=(
        'django.contrib.staticfiles',  # better runserver
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'django.contrib.sitemaps',
        'django.contrib.auth',
        'django.contrib.admin',
        'sniplates',
        'pipeline',
        'varlet',
        'jobs',
    ) + DEBUG_APPS,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    HAYSTACK_CONNECTIONS={
        'default': {
            'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
            'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
        },
    },
    STATIC_ROOT=os.path.join(BASE_DIR, '__static__'),
    MEDIA_ROOT=os.path.join(BASE_DIR, '__uploads__'),
    STATIC_URL='/__static__/',
    MEDIA_URL='/__uploads__/',
    STATICFILES_DIRS=[
        os.path.join(BASE_DIR, 'static'),
    ],
    STATICFILES_FINDERS=[
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'pipeline.finders.PipelineFinder',
    ],
    STATICFILES_STORAGE='pipeline.storage.PipelineCachedStorage',
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
    ],
    PIPELINE={
        # 'PIPELINE_ENABLED': True,
        # 'PIPELINE_COLLECTOR_ENABLED': True,
        'SHOW_ERRORS_INLINE': True,
        'CSS_COMPRESSOR': None,
        'JS_COMPRESSOR': None,
        'STYLESHEETS': {
            'application': {
                'source_filenames': [
                    'css/normalize.css',
                    'css/skeleton.css',
                    'css/logo.css',
                ],
                'output_filename': 'css/application.css',
            }
        },
        'JAVASCRIPT': {
            'application': {
                'source_filenames': [],
                'output_filename': 'js/application.js',
            }
        }
    },
    REST_FRAMEWORK={
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        ),
        'PAGE_SIZE': 25,
        'COMPACT_JSON': False,
    }
)



def lazy_urls():
    from django.conf.urls import url, include
    from django.contrib import admin
    from rest_framework.routers import DefaultRouter
    try:
        from fastsitemaps.views import sitemap
    except ImportError:
        from django.contrib.sitemaps.views import sitemap
    from varlet.urls import urlpatterns as varlet_urls
    from varlet.sitemaps import PageSitemap

    router = DefaultRouter()

    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^api/', include(router.urls)),
        url(r'^sitemap.xml$', sitemap, {'sitemaps': {'pages': PageSitemap()}}, name='xml_sitemap'),
        url(r'^', include(varlet_urls)),
    ]
    if DEBUG:
        from debug_toolbar import urls as djdt
        urlpatterns = [
            url(r'^__djdt__/', include(djdt))
        ] + urlpatterns
    return urlpatterns
from django.utils.functional import SimpleLazyObject
# Can't use lazy(lazy_urls, list) because it doesn't implement __iter__?
urlpatterns = SimpleLazyObject(lazy_urls)



from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
