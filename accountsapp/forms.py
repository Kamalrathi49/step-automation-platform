from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models.fields import files
from django.forms.fields import ChoiceField
from accountsapp.models import *
from stepautomationapp.models import *
from django_countries.fields import CountryField



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


class UserDataForm(forms.ModelForm):
    company = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',  'placeholder': 'Company'}), label='')
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',  'placeholder': 'City'}), label='')
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',  'placeholder': 'Address Line'}), label='')
    zipcode = forms.CharField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',  'placeholder': 'Zip Code'}), label='')
    profilepic = forms.FileField(required=False, widget=forms.ClearableFileInput({
        'class': 'form-control', 'name': 'profilepic',
        }), label='')

    class Meta:
        model = UserData
        exclude = ['userrelation',]
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(UserDataForm, self).__init__(*args, **kwargs)
        self.fields['country'].label = ""