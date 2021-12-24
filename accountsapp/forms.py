from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import DateInput
from .models import *


class RegisterForm(UserCreationForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={
     'class': 'form-control', 'placeholder': 'Email Address'
    }), label='')

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',  'placeholder': 'Password'}),label='')
        
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm Password'}),label='')

    class Meta:
        model = User
        fields = ("email", 'password1', 'password2' )


class LoginForm(forms.Form):
    username = forms.EmailField(max_length=99, widget=forms.EmailInput(attrs={
        'class': 'form-control mb-2',  'placeholder': 'Email'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-2',  'placeholder': 'Password'}), label='')