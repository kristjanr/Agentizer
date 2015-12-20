from django.utils.safestring import mark_safe
from django_tables2 import tables
import django_tables2

from app.models import Tour


class TourTable(tables.Table):
    def render_ref_number(self, record):
        return mark_safe('<a href=%s>%s</a>' % (
            record.id,
            record.ref_number
        ))

    class Meta:
        model = Tour
        exclude = ('id')
        attrs = {"class": "paleblue"}

    sent = django_tables2.BooleanColumn(orderable=False)
    accepted = django_tables2.BooleanColumn(null=True, orderable=False)
