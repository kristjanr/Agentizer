from django.utils.safestring import mark_safe
from django_tables2 import tables
import django_tables2
from django.utils.translation import ugettext_lazy as _
from django_tables2.utils import cached_property

from app.models import Tour, GuideTour


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
        attrs = {"class": "paleblue"}

    name = django_tables2.Column(accessor='guide.name')
    phone_number = django_tables2.Column(accessor='guide.phone_number')
    email = django_tables2.Column(accessor='guide.email')


class TourTable(tables.Table):
    def render_ref_number(self, record):
        return mark_safe('<a href=%s>%s</a>' % (
            record.id,
            record.ref_number
        ))

    class Meta:
        model = Tour
        exclude = (
            'id',
            'description',
            'user',
        )
        attrs = {'class': 'paleblue'}
        verbose_name_plural = 'stability_dashboard'

    sent = django_tables2.BooleanColumn(orderable=False, verbose_name=_('SMS sent'))
    accepted = django_tables2.BooleanColumn(null=True, orderable=False, verbose_name=_('Guide accepted'))
