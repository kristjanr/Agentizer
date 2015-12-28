from django.utils.safestring import mark_safe
from django_tables2 import tables
import django_tables2
from django.utils.translation import ugettext_lazy as _

from app.models import Tour, GuideTour, Guide


class GuideTable(tables.Table):
    def render_name(self, record):
        return mark_safe('<a href=%s>%s</a>' % (
            record.get_absolute_url(),
            record.name
        ))

    class Meta:
        model = Guide
        exclude = (
            'id',
        )
        sequence = (
            'name',
            'phone_number',
            'email',
        )
        order_by = ('name',)
        attrs = {"class": "paleblue"}


class GuideTourTable(tables.Table):
    class Meta:
        model = GuideTour
        exclude = (
            'id',
            'uid',
            'guide',
            'tour',
        )
        sequence = (
            'name',
            'phone_number',
            'email',
            'seen',
            'answer',
        )
        order_by = ('-seen', 'answer',)

        attrs = {"class": "paleblue"}

    name = django_tables2.Column(accessor='guide.name')
    phone_number = django_tables2.Column(accessor='guide.phone_number')
    email = django_tables2.Column(accessor='guide.email')


class TourTable(tables.Table):
    def render_ref_number(self, record):
        return mark_safe('<a href=%s>%s</a>' % (
            record.get_absolute_url(),
            record.ref_number
        ))

    class Meta:
        model = Tour
        exclude = (
            'id',
            'description',
            'user',
        )
        order_by = ('start_time', 'end_time')
        attrs = {'class': 'paleblue'}
        verbose_name_plural = 'stability_dashboard'

    sent = django_tables2.BooleanColumn(orderable=False, verbose_name=_('Message sent'))
    accepted = django_tables2.BooleanColumn(null=True, orderable=False, verbose_name=_('Guide accepted'))
