from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import User


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)


class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class OtpForm(forms.Form):
    code = forms.CharField(max_length=6, min_length=6, label=_('code'),
                           widget=forms.PasswordInput())

    def __init__(self, request, *args, **kwargs):
        assert request.user.is_authenticated(), (
            'OtpForm shoud never be used for unauthenticated users')

        self.request = request
        super().__init__(*args, **kwargs)

    def clean_code(self):
        user = self.request.user
        code = self.cleaned_data.get('code')

        if not user.otp_verify(code):
            raise forms.ValidationError(_('Invalid code'))
