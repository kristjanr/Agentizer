from django.db import models


class Guide(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField(blank=True)


class Tour(models.Model):
    ref_number = models.CharField(max_length=100)
    group_size = models.IntegerField()
    group_name = models.CharField(max_length=100, null=True)
    language = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    meeting_point = models.CharField(max_length=300)
    ending_point = models.CharField(max_length=300)
    description = models.CharField(max_length=500)


class GuideTour(models.Model):
    uid = models.CharField(unique=True, max_length=8, default=None)
    guide = models.ForeignKey(Guide)
    tour = models.ForeignKey(Tour)
    seen = models.BooleanField(default=False)
    answer = models.NullBooleanField(null=True)
