from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, widget=forms.EmailInput(attrs={'placeholder' : 'Email'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'placeholder' : 'Password'})

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, widget=(forms.TextInput(attrs={'placeholder' : 'First Name'})))
    last_name = forms.CharField(required=True, widget=(forms.TextInput(attrs={'placeholder' : 'Last Name'})))
    coupon = forms.CharField(max_length=10, required=False, widget=(forms.TextInput(attrs={'placeholder' : 'Coupon Code'})))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'coupon']
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})

    def clean(self):
        form_data = self.cleaned_data
        if form_data['coupon']:
            if not User.objects.filter(username=form_data['coupon']).exists():
                self._errors['coupon'] = 'Invalid Coupon Code'
        return form_data