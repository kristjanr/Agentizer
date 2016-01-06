# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_add_guides_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='guidetour',
            name='uid',
            field=models.CharField(unique=True, max_length=8, default=None),
        ),
    ]
