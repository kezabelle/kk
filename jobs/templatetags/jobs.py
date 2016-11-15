# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import swapper
from django import template

register = template.Library()

@register.assignment_tag(takes_context=True)
def get_jobs(context):
    """
    Largely exists for me to prototype this out ...
    """
    if 'GET_JOBS' in context:
        return context['GET_JOBS']
    else:
        jobs = swapper.load_model('jobs', 'Job').objects.all()
        context['GET_JOBS'] = jobs
        return jobs
