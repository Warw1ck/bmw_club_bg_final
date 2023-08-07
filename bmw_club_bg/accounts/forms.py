from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _


class CustomPasswordChangeForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
