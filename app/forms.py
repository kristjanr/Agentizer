# forms.py
from datetimewidget.widgets import DateTimeWidget
from django import forms
import account.forms

from app.models import Tour, Guide
from django.utils.translation import ugettext as _


class SignupForm(account.forms.SignupForm):
    company_name = forms.CharField(min_length=3, max_length=100, label=_('Company name'))


class MyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_class()

    def add_class(self):
        for f in self.fields.values():
            w = f.widget
            w.attrs.update({'class': 'form-control'})


class TourForm(MyForm):
    class Meta:
        model = Tour
        fields = [
            'ref_number',
            'group_size',
            'group_name',
            'language',
            'start_time',
            'end_time',
            'meeting_point',
            'ending_point',
            'description',
        ]
        dateTimeOptions = {
            'format': 'yyyy-mm-dd hh:ii',
            'autoclose': True,
            'weekStart': 1,
        }
        widget = DateTimeWidget(options=dateTimeOptions, bootstrap_version=3)
        widgets = {
            'start_time': widget,
            'end_time': widget
        }


class GuideForm(MyForm):
    class Meta:
        model = Guide
        fields = [
            'name',
            'phone_number',
            'email',
        ]
