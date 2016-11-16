# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls import url
from .views import job_detail, job_list

job_detail_url = url(
    regex='^(?P<slug>[-a-zA-Z0-9_]+)/$',
    view=job_detail,
    name="job_detail",
    kwargs={}
)
job_list_url = url(
    regex='^$',
    view=job_list,
    name="job_list",
    kwargs={}
)
current_app = "jobs"
urlpatterns = [
    job_detail_url,
    job_list_url,
]
