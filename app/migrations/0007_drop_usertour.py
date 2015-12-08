# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


def set_users_to_tours(apps, schema_editor):
    UserTour = apps.get_model('app', 'UserTour')
    for usertour in UserTour.objects.all():
        usertour.tour.user = usertour.user
        usertour.tour.save()
    Tour = apps.get_model('app', 'Tour')
    Tour.objects.filter(user=None).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0006_profile_usertour'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='user',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(set_users_to_tours),
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
