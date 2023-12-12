from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.forms import widgets

from apps.entry.forms import grouping
from apps.entry.widgets import BooleanWidget
from apps.organization.models import Organization


class RegistrationForm(forms.Form):
    template_name = 'entry/components/forms/scout.html'

    # Personal
    username = forms.CharField(widget=widgets.TextInput, max_length=150, validators=[UnicodeUsernameValidator()])
    password = forms.CharField(widget=widgets.PasswordInput, max_length=128)
    password_validate = forms.CharField(widget=widgets.PasswordInput, label="Verify Password")
    first_name = forms.CharField(widget=widgets.TextInput, label="First Name", min_length=3, max_length=150)
    last_name = forms.CharField(widget=widgets.TextInput, label="Last Name", min_length=3, max_length=150)
    email = forms.EmailField(widget=widgets.EmailInput, label="Email Address")
    email_validate = forms.EmailField(widget=widgets.EmailInput, label="Verify Email Address")

    # Organization
    create_new_org = forms.BooleanField(widget=BooleanWidget(), required=False, label="Create New?",
                                        label_suffix="")
    org_name = forms.CharField(widget=widgets.TextInput, min_length=5, max_length=250, label="Organization Name")
    org_reg_id = forms.CharField(widget=widgets.TextInput, label="Registration Code", min_length=6, max_length=6, required=False)

    grouping("Personal", [username, password, password_validate, first_name, last_name, email_validate, email])
    grouping("Organization", [create_new_org, org_name, org_reg_id])

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        except User.MultipleObjectsReturned:
            raise ValidationError('Username already exists and multiple users have it.')
        raise ValidationError('Username already exists.')

    def clean_password_validate(self):
        if self.cleaned_data['password_validate'] != self.cleaned_data['password']:
            raise ValidationError('Passwords must match.')
        return self.cleaned_data['password_validate']

    def clean_email_validate(self):
        if self.cleaned_data['email_validate'] != self.cleaned_data['email']:
            raise ValidationError('Emails must match.')
        return self.cleaned_data['email_validate']

    def clean_team_reg_id(self):
        reg_uuid = self.cleaned_data['org_reg_id']
        org_name = self.cleaned_data['org_name']
        if str(Organization.objects.get(name=org_name).reg_id)[:6] != reg_uuid[:6]:
            raise ValidationError('Incorrect RegID for Org: ' + str(org_name) + '.')
        return uuid
