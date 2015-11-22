# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.sites.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('domain', models.CharField(verbose_name='domain name', max_length=100, validators=[django.contrib.sites.models._simple_domain_name_validator])),
                ('name', models.CharField(verbose_name='display name', max_length=50)),
            ],
            options={
                'verbose_name': 'site',
                'db_table': 'django_site',
                'verbose_name_plural': 'sites',
                'ordering': ('domain',),
            },
            managers=[
                ('objects', django.contrib.sites.models.SiteManager()),
            ],
        ),
    ]
