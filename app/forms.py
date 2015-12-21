# forms.py
from datetimewidget.widgets import DateTimeWidget
from django import forms
import account.forms

from app.models import Tour
from django.utils.translation import ugettext_lazy as _


class SignupForm(account.forms.SignupForm):
    company_name = forms.CharField(min_length=3, max_length=100)


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
        # labels = {
        #             'ref_number': _('Reference number'),
        #             'group_size': _('Group size'),
        #             'group_name': _('Group name'),
        #             'language': _('Language'),
        #             'start_time': _('Start time'),
        #         }
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
