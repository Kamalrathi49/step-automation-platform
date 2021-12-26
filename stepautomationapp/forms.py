from django.contrib.auth.models import User
from django.db.models import fields
from django.forms.widgets import CheckboxInput
from .models import  *
from django import forms

CHOICE_LEAD = [
            ('GUIDE', 'Guide'),
            ('GUIDEE', 'Guidee'),
            ('BACK OFFICE', 'Backoffice'),
    ]

class Stepsform(forms.ModelForm):
    count = forms.FloatField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'style': 'width: 40%;',
        'placeholder': 'Ex. 1.0',
    }),label='Step Number')
    description = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'style': 'height:50px;',
        'placeholder': 'Enter Step Description',
    }),label='Description')
    instruction = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Detailed Step Instructions',
        'rows':6, 'cols':15,
    }),label='Instructions')
    visibility = forms.BooleanField( required=False, label='Step Visibile')
    download = forms.BooleanField( required=False,  label='Download control visible')

    step_file = forms.FileField(widget=forms.ClearableFileInput({
        'class': 'form-control',
        'name': 'step_file',
        'style': 'width:70%;'
        }), label='File for download')
    upload = forms.BooleanField(required=False, label='Upload control visible')

    class Meta:
        model = Steps
        exclude = ['user', 'project_template']
        fields = '__all__'


class DocumentsForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'style': 'margin-bottom: 16px;',
        'placeholder': 'Enter Standard File Description',
    }),label='Description')
    step_file = forms.FileField(widget=forms.ClearableFileInput(
        {'class': 'form-control',
         'name': 'step_document',
         'style': 'width:80%'
         }), label='File')

    class Meta:
        model = Documents
        exclude = ('user',)
        fields = '__all__'


class CustomersForm(forms.ModelForm):
    class Meta:
        model = Customers
        exclude = ('user',)
        fields = '__all__'


class ProjectTemplateForm(forms.ModelForm):
    
    description  = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'style': 'margin-bottom: 20px;',
        'placeholder': 'Enter Standard Workflow Name'
    }))
    lead = forms.ChoiceField(choices=CHOICE_LEAD, widget=forms.Select(attrs={
        'class': 'form-control',
        'style': 'cursor: pointer;',
        }), label='Lead')
    class Meta:
        model = ProjectTemplate
        exclude = ('user',)
        fields = '__all__'

   

class CustomerWorkflowForm(forms.ModelForm):
    
    CHOICE_STATUS = [
            ('INVITE SENT', 'Invite Sent'),
            ('INVITE NOT SENT', 'Invite not sent'),
            ('ONGOING', 'Ongoing'),
            ('FINISHED', 'Finished'),
            ('CANCELLED', 'Cancelled'),
    ]
    
    status = forms.ChoiceField(choices=CHOICE_STATUS, widget=forms.Select(attrs={
        'class': 'form-control',
        'style': 'cursor: pointer; margin-botton:16px;',
        }), label='Status')
    description  = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'style': 'margin-bottom:;',
        'placeholder': 'Enter Customer Workflow Name'
         }))
    lead = forms.ChoiceField(choices=CHOICE_LEAD, widget=forms.Select(attrs={
        'class': 'form-control',
        'style': 'cursor: pointer;',
        }), label='Lead')
    class Meta:
        model = CustomerWorkflow
        exclude = ('user',)
        fields = '__all__'

    def __init__(self,user,*args,**kwargs):
        super (CustomerWorkflowForm,self ).__init__(*args,**kwargs)
        self.fields['customer'].queryset = Customers.objects.filter(user=user)


class CustomerStepsform(forms.ModelForm):

    
    count = forms.FloatField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'style': 'width: 40%;',
        'placeholder': 'Ex. 1.0',
    }),label='Step Number')
    description = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'style': 'height:50px;',
        'placeholder': 'Enter Step Description',
    }),label='Description')
    instruction = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Detailed Step Instructions',
        'rows':6, 'cols':15,
    }),label='Instructions')
    visibility = forms.BooleanField( required=False, label='Step Visibile')
    download = forms.BooleanField( required=False,  label='Download control visible')
    step_file = forms.FileField(widget=forms.ClearableFileInput({
        'class': 'form-control',
        'name': 'step_file',
        'style': 'width:70%;'
        }), label='File for download')
    upload = forms.BooleanField(required=False, label='Upload control visible')

    class Meta:
        model = CustomerSteps
        exclude = ['user', 'customerworkflow']
        fields = '__all__'

