# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings


def set_default_language(apps, schema_editor):
    Account = apps.get_model('account', 'Account')
    for account in Account.objects.all():
        account.language = 'et'
        account.save()

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0009_drop_usertour'),
    ]

    operations = [
        migrations.RunPython(set_default_language),
    ]
