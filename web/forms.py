import random
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
from parsley.decorators import parsleyfy
from web.models import Subscriber


class UserSearchTimeForm(forms.Form):
    from_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(attrs={
            'id': "datepicker-from",
            'placeholder': 'Start Date',
            'class': 'form-control',
            'aria-describedby': 'From Date Field',
        }),
    )

    to_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(attrs={
            'id': "datepicker-to",
            'placeholder': 'End Date',
            'class': 'form-control',
            'aria-describedby': 'To Date Field',
        })
    )

# edit form
@parsleyfy
class EditSubscriberForm(forms.Form):
    ROLES = (('Admin', 'Admin'), ('User', 'User'))
    LOCAL = (('Yes', 'Yes'), ('No', 'No'))
    CONN_STATUS = (('Authorized', 'Authorized'), ('Blocked', 'Blocked'))

    name = forms.CharField(label='Name')
    imsi = forms.RegexField(
        label="IMSI",
        help_text='10-digit number on SIM card',
        regex='[0-9]*',
        min_length=10,
        max_length=10,
        error_messages={'required': "Please Enter 10 digit number"},
        strip=True,
    )
    authorization_status = forms.ChoiceField(
        choices=CONN_STATUS,
        label='Connection Status',
    )
    rate_limit = forms.DecimalField()
    msisdn = forms.RegexField(
        label="Phone Number",
        regex=r'[0-9]*',
        min_length=4,
        strip=True,
    )

# add form
@parsleyfy
class AddSubscriberForm(forms.Form):
    ROLES = (('Admin', 'Admin'), ('User', 'User'))
    LOCAL = (('Yes', 'Yes'), ('No', 'No'))
    CONN_STATUS = (('Authorized', 'Authorized'), ('Blocked', 'Blocked'))

    name = forms.CharField(label='Name')
    imsi = forms.RegexField(
        label="IMSI",
        help_text='10-digit number on SIM card',
        regex='[0-9]*',
        min_length=10,
        max_length=10,
        error_messages={'required': "Please Enter 10 digit number"},
        strip=True,
    )
    authorization_status = forms.ChoiceField(
        choices=CONN_STATUS,
        label='Connection Status',
    )
    rate_limit = forms.DecimalField()
    msisdn = forms.RegexField(
        label="Phone Number",
        regex=r'[0-9]*',
        min_length=4,
        strip=True,
    )

    def clean_imsi(self):
        """Ensure the imsi provided meets application uniqueness constraints
        """
        imsi = self.cleaned_data["imsi"]

        if User.objects.filter(username=imsi).exists():
            raise forms.ValidationError(
                "The IMSI {} already exists".format(imsi)
            )

        return imsi


# delete form
@parsleyfy
class DeleteSubscriberForm(forms.Form):
    ROLES = (('Admin', 'Admin'), ('User', 'User'))
    LOCAL = (('Yes', 'Yes'), ('No', 'No'))
    CONN_STATUS = (('Authorized', 'Authorized'), ('Blocked', 'Blocked'))

    name = forms.CharField(label='Name')
    imsi = forms.RegexField(label="IMSI", help_text='10-digit number on SIM card', regex='[0-9]{10}', min_length=10, max_length=10, error_messages = {
        'required':"Please Enter 10 digit number"
    }, strip=True, widget=forms.HiddenInput())
    role = forms.ChoiceField(choices=ROLES)
    connection_status = forms.ChoiceField(choices=CONN_STATUS, label='Connection Status')
    rate_limit = forms.DecimalField()

    def clean_name(self):
        name = self.cleaned_data['name']
        return name
