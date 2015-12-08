# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_set_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertour',
            name='tour',
        ),
        migrations.RemoveField(
            model_name='usertour',
            name='user',
        ),
        migrations.AlterField(
            model_name='tour',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UserTour',
        ),
    ]
