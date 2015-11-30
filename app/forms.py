# forms.py

from django import forms

import account.forms


class SignupForm(account.forms.SignupForm):

    company_name = forms.CharField(min_length=3, max_length=100)

