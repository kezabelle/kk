# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class JobsConfig(AppConfig):
    name = 'jobs'
    verbose_name = _("jobs")
