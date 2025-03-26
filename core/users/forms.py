from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)
    
from django import forms

class OTPTokenForm(forms.Form):
    token = forms.CharField(
        label='Token 2FA',
        max_length=6,
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder': '123456'})
    )

