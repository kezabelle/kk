# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import swapper
from django.contrib import admin


class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'start', 'end', 'get_short_description')
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(swapper.load_model('jobs', 'Job'), admin_class=JobAdmin)
