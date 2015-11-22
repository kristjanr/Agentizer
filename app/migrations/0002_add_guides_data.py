# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

guide_data = [{'phone_number': '+37253498963', 'email': 'kristjan.r@gmail.com', 'name': 'Kristjan Roosild'}, {'phone_number': '+3725216544', 'email': 'dana.neemre@viahansa.com', 'name': 'Dana Neemre'}, {'phone_number': '+3725206098', 'email': 'raimo@telliskivi.eu', 'name': 'Raimo Matvere'}, {'phone_number': '+37253446904', 'email': 'a-kakukk@microsoft.com', 'name': 'Kadri Kukk'}, {'phone_number': '+37256303670', 'email': '', 'name': 'Riin Kirt'}]


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
