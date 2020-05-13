from django import forms


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

class ModalForm(forms.Form):
    name = forms.CharField(label='Your name')
    phoneNumber = forms.NumberInput()
    display = forms.CharField(label='Display name')
    localNonLocal = forms.CharField(label='Local or non local')
    role = forms.CharField(label='Role')
    connected = forms.CharField(label='Connected')
    activeStatus = forms.DateTimeField(label='Last active')
