# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv

from django.db import migrations


def insert_guides(apps, schema_editor):
    """Populate the sites model"""
    Guide = apps.get_model('app', 'Guide')
    Guide.objects.all().delete()

    with open('guides_demo.csv') as fp:
        guides = csv.reader(fp)
        for guide in guides:
            Guide.objects.create(name=guide[0], phone_number=guide[1], email=guide[2])


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_guides)
    ]
