# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20151122_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='group_name',
            field=models.CharField(null=True, max_length=100),
        ),
    ]
