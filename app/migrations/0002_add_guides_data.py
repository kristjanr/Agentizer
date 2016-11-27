# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

guide_data = [
    {'phone_number': '+37253498963', 'email': 'kristjan.r@gmail.com', 'name': 'Kristjan Roosild'},
    {'phone_number': '+6587424784', 'email': 'kristjan.r+singapore@gmail.com', 'name': 'Kristjan Roosild'}]


def insert_guides(apps, schema_editor):
    Guide = apps.get_model('app', 'Guide')
    Guide.objects.all().delete()

    for guide in guide_data:
        Guide.objects.create(**guide)


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_guides)
    ]
