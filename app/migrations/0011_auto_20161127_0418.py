# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_set_default_language'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tour',
            options={'verbose_name': 'stability_dashboard', 'verbose_name_plural': 'stability_dashboard'},
        ),
        migrations.AddField(
            model_name='guidetour',
            name='delivered',
            field=models.NullBooleanField(verbose_name='Delivered'),
        ),
        migrations.AddField(
            model_name='guidetour',
            name='failed',
            field=models.NullBooleanField(verbose_name='Sending failed'),
        ),
        migrations.AddField(
            model_name='guidetour',
            name='sent',
            field=models.NullBooleanField(verbose_name='Sent'),
        ),
        migrations.AddField(
            model_name='guidetour',
            name='sms_unique_id',
            field=models.CharField(default=None, max_length=44, unique=True),
        ),
        migrations.AlterField(
            model_name='guide',
            name='email',
            field=models.EmailField(verbose_name='E-mail', blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='guide',
            name='name',
            field=models.CharField(verbose_name='Name', max_length=100),
        ),
        migrations.AlterField(
            model_name='guide',
            name='phone_number',
            field=models.CharField(verbose_name='Phone number', max_length=100),
        ),
        migrations.AlterField(
            model_name='guidetour',
            name='answer',
            field=models.NullBooleanField(verbose_name='Answer'),
        ),
        migrations.AlterField(
            model_name='guidetour',
            name='seen',
            field=models.BooleanField(default=False, verbose_name='Seen'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='company_name',
            field=models.CharField(verbose_name='Company name', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(verbose_name='Phone number', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(verbose_name='User', to=settings.AUTH_USER_MODEL, related_name='profile'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='description',
            field=models.CharField(verbose_name='Description', max_length=500),
        ),
        migrations.AlterField(
            model_name='tour',
            name='end_time',
            field=models.DateTimeField(verbose_name='End time'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='ending_point',
            field=models.CharField(verbose_name='Ending point', max_length=300),
        ),
        migrations.AlterField(
            model_name='tour',
            name='group_name',
            field=models.CharField(verbose_name='Group name', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tour',
            name='group_size',
            field=models.IntegerField(verbose_name='Group size'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='language',
            field=models.CharField(verbose_name='Language', max_length=100),
        ),
        migrations.AlterField(
            model_name='tour',
            name='meeting_point',
            field=models.CharField(verbose_name='Meeting point', max_length=300),
        ),
        migrations.AlterField(
            model_name='tour',
            name='ref_number',
            field=models.CharField(verbose_name='Reference number', max_length=100),
        ),
        migrations.AlterField(
            model_name='tour',
            name='start_time',
            field=models.DateTimeField(verbose_name='Start time'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='user',
            field=models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL),
        ),
    ]
