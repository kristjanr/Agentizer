from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Guide(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    phone_number = models.CharField(max_length=100, verbose_name=_('Phone number'))
    email = models.EmailField(blank=True, verbose_name=_('E-mail'))

    def get_absolute_url(self):
        return "/guide/%i/" % self.id


class Tour(models.Model):
    ref_number = models.CharField(max_length=100, verbose_name=_('Reference number'))
    group_size = models.IntegerField(verbose_name=_('Group size'))
    group_name = models.CharField(max_length=100, null=True, verbose_name=_('Group name'))
    language = models.CharField(max_length=100, verbose_name=_('Language'))
    start_time = models.DateTimeField(verbose_name=_('Start time'))
    end_time = models.DateTimeField(verbose_name=_('End time'))
    meeting_point = models.CharField(max_length=300, verbose_name=_('Meeting point'))
    ending_point = models.CharField(max_length=300, verbose_name=_('Ending point'))
    description = models.CharField(max_length=500, verbose_name=_('Description'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("User"))

    def get_absolute_url(self):
        return "/tour/%i/" % self.id

    @property
    def sent(self):
        if self.guidetour_set.all():
            return True
        return False

    @property
    def accepted(self):
        for guidetour in self.guidetour_set.all():
            if guidetour.answer:
                return True
        else:
            return False

    class Meta:
        verbose_name = 'stability_dashboard'
        verbose_name_plural = 'stability_dashboard'


class GuideTour(models.Model):
    uid = models.CharField(unique=True, max_length=8, default=None)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False, verbose_name=_('Seen'))
    answer = models.NullBooleanField(null=True, verbose_name=_('Answer'))


class Profile(models.Model):
    company_name = models.CharField(max_length=100, verbose_name=_('Company name'))
    phone_number = models.CharField(max_length=100, verbose_name=_('Phone number'))
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', verbose_name=_('User'), on_delete=models.CASCADE)
