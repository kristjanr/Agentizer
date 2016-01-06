# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def insert_sites(apps, schema_editor):
    """Populate the sites model"""
    Site = apps.get_model('sites', 'Site')
    Site.objects.all().delete()

    # Register SITE_ID = 1
    Site.objects.create(id=1, domain='agentizer.com', name='Agentizer.com')
    Site.objects.create(id=2, domain='agentizer.herokuapp.com', name='agentizer.herokuapp.com')


class Migration(migrations.Migration):
    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_sites)
    ]
