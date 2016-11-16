# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import swapper
from django.db import migrations, models

template = 'varlet/pages/layouts/default.html'
pages = (
    {'url': '', 'template': template},
    {'url': 'about', 'template': template},
    {'url': 'open-source', 'template': template}
)

def create_pages(apps, schema_editor):
    model = apps.get_model('varlet', 'Page')

    for page in pages:
        model.objects.get_or_create(**page)

def delete_pages(apps, schema_editor):
    model = apps.get_model('varlet', 'Page')
    for page in pages:
        model.objects.filter(url=page['url']).delete()

class Migration(migrations.Migration):
    dependencies = [
        swapper.dependency('varlet', 'Page')
    ]

    operations = [
        migrations.RunPython(create_pages, delete_pages),
    ]
