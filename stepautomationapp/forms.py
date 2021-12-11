from .models import  ProjectTemplate, Steps, Documents, Customers
from django import forms


class Stepsform(forms.ModelForm):
    DISPLAY_Visibity_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No')
    ]
    visibility = forms.ChoiceField(choices=DISPLAY_Visibity_CHOICES, widget=forms.RadioSelect(),
                                        label='Steps Visibile')
    download = forms.ChoiceField(choices=DISPLAY_Visibity_CHOICES, widget=forms.RadioSelect(), label='Download')
    upload = forms.ChoiceField(choices=DISPLAY_Visibity_CHOICES, widget=forms.RadioSelect(), label='Upload')
    step_file = forms.FileField(widget=forms.ClearableFileInput(
        {'class': 'form-control form-control-lg', 'name': 'step_file'}), label='File for download')

    class Meta:
        model = Steps
        exclude = ['user', 'project_template']
        fields = '__all__'


class DocumentsForm(forms.ModelForm):
    DISPLAY_Visibity_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No')
    ]
    notarize = forms.ChoiceField(choices=DISPLAY_Visibity_CHOICES, widget=forms.RadioSelect(), label='Notarize',
                                 initial={'notarize': 'No'})
    apostille = forms.ChoiceField(choices=DISPLAY_Visibity_CHOICES, widget=forms.RadioSelect(), label='Apostille',
                                  initial={'apostille': 'No'})
    step_file = forms.FileField(widget=forms.ClearableFileInput(
        {'class': 'form-control form-control-lg', 'name': 'step_document'}))

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
    CHOICE_LEAD = [
            ('GUIDE', 'Guide'),
            ('GUIDEE', 'Guidee'),
            ('BACK OFFICE', 'Backoffice'),
    ]
    
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

   

