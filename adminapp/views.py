from django.shortcuts import render
from stepautomationapp.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/')
def dashboard(request):
    users = User.objects.all()
    ctx = {'users':users}
    return render( request, 'admin/admindashboard.html', ctx)

@login_required(login_url='/')
def accounts(request):
    users = User.objects.all()
    userdata = UserData.objects.all()
    usercount = User.objects.all().count()
    ctx = {'users': users, 'usercount': usercount, 'userdata': userdata}
    return render(request, 'admin/accounts_page.html', ctx )

@login_required(login_url='/')
def standardfiles(request):
    standardfiles = Documents.objects.all()
    standardfilescount = Documents.objects.all().count()
    ctx = {'standardfiles': standardfiles, 'standardfilescount': standardfilescount}
    return render(request, 'admin/standardfilespage.html', ctx )

@login_required(login_url='/')
def standardsteps(request):
    standardsteps = Steps.objects.all()
    standardstepscount = Steps.objects.all().count()
    ctx = {'standardsteps': standardsteps, 'standardstepscount': standardstepscount}
    return render(request, 'admin/standardstepspage.html', ctx )

@login_required(login_url='/')
def standardworkflows(request):
    standardworkflow = ProjectTemplate.objects.all()
    standardworkflowcount = ProjectTemplate.objects.all().count()
    ctx = {'standardworkflows': standardworkflow, 'workflowcount': standardworkflowcount}
    return render(request, 'admin/standardworkflow.html', ctx )

@login_required(login_url='/')
def customerworkflows(request):
    customerworkflow = CustomerWorkflow.objects.all()
    customerworkflowcount = CustomerWorkflow.objects.all().count()
    ctx = {'customerworkflows': customerworkflow, 'customerworkflowcount': customerworkflowcount}
    return render(request, 'admin/customerworkflow_page.html', ctx )

@login_required(login_url='/')
def customersteps(request):
    customersteps = CustomerSteps.objects.all()
    customerstepscount = CustomerSteps.objects.all().count()
    ctx = {'customersteps': customersteps, 'customerstepscount': customerstepscount}
    return render(request, 'admin/customersteps.html', ctx )