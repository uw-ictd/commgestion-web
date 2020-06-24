from django import forms
from parsley.decorators import parsleyfy


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
class ModalEditForm(forms.Form):
    ROLES = (('Admin', 'Admin'), ('User', 'User'))
    LOCAL = (('Yes', 'Yes'), ('No', 'No'))
    CONN_STATUS = (('Online', 'Online'), ('Offline', 'Offline'), ('Blocked', 'Blocked'))

    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email Address')
    imsi = forms.RegexField(label="IMSI", help_text='10-digit number on SIM card', regex='[0-9]{10}', min_length=10, max_length=10, error_messages = {
        'required':"Please Enter 10 digit number"
    }, strip=True)
    # guti = forms.RegexField(label="GUTI", help_text='5 digits ???? following IMSI value', regex=r'^[0-9]{5}$', strip=True)
    # phone = forms.RegexField(label="Phone Number", regex=r'^[0-9]{5}$', strip=True)
    # resident_status = forms.ChoiceField(choices=LOCAL, label='Local Resident?')
    # password = forms.CharField(widget = forms.PasswordInput())
    role = forms.ChoiceField(choices=ROLES)
    connection_status = forms.ChoiceField(choices=CONN_STATUS, label='Connection Status')
    rate_limit = forms.DecimalField()

# add form
@parsleyfy
class ModalForm(forms.Form):
    ROLES = (('Admin', 'Admin'), ('User', 'User'))
    LOCAL = (('Yes', 'Yes'), ('No', 'No'))
    CONN_STATUS = (('Online', 'Online'), ('Offline', 'Offline'), ('Blocked', 'Blocked'))

    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email Address')
    imsi = forms.RegexField(label="IMSI", help_text='10-digit number on SIM card', regex='[0-9]{10}', min_length=10, max_length=10, error_messages = {
         'required':"Please Enter 10 digit number"
    }, strip=True)
    role = forms.ChoiceField(choices=ROLES)
    connection_status = forms.ChoiceField(choices=CONN_STATUS, label='Connection Status')
    rate_limit = forms.DecimalField()
    # guti = forms.RegexField(label="GUTI", help_text='5 digits ???? following IMSI value', regex=r'^[0-9]{5}$', strip=True)
    # phone = forms.RegexField(label="Phone Number", regex=r'^[0-9]{5}$', strip=True)
    # resident_status = forms.ChoiceField(choices=LOCAL, label='Local Resident?')

# delete form
@parsleyfy
class ModalDeleteForm(forms.Form):
    ROLES = (('Admin', 'Admin'), ('User', 'User'))
    LOCAL = (('Yes', 'Yes'), ('No', 'No'))
    CONN_STATUS = (('Online', 'Online'), ('Offline', 'Offline'), ('Blocked', 'Blocked'))

    first_name = forms.CharField(label='First Name')

    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email Address')
    imsi = forms.RegexField(label="IMSI", help_text='10-digit number on SIM card', regex='[0-9]{10}', min_length=10, max_length=10, error_messages = {
        'required':"Please Enter 10 digit number"
    }, strip=True)
    role = forms.ChoiceField(choices=ROLES)
    connection_status = forms.ChoiceField(choices=CONN_STATUS, label='Connection Status')
    rate_limit = forms.DecimalField()

    def clean_first_name(self):
        name = self.cleaned_data['first_name']
        return name;

    def clean_last_name(self):
        lastName = self.cleaned_data['last_name']
        return lastName
