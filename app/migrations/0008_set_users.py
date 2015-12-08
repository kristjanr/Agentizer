# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings


def set_users_to_tours(apps, schema_editor):
    UserTour = apps.get_model('app', 'UserTour')
    for usertour in UserTour.objects.all():
        usertour.tour.user = usertour.user
        usertour.tour.save()
    Tour = apps.get_model('app', 'Tour')
    Tour.objects.filter(user__isnull=True).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0007_add_user_to_tour'),
    ]

    operations = [
        migrations.RunPython(set_users_to_tours),
    ]
