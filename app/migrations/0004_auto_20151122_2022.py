# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_guidetour_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guidetour',
            name='answer',
            field=models.NullBooleanField(),
        ),
    ]
