from django import forms
from django.contrib.auth.forms import AuthenticationForm



class LoginForm(forms.Form):
    username = forms.EmailField(max_length=99, widget=forms.EmailInput(attrs={
        'class': 'form-control mb-2',  'placeholder': 'Email'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-2',  'placeholder': 'Password'}), label='')