from django.shortcuts import render
from stepautomationapp.models import *
from django.contrib.auth.models import User
# Create your views here.

def dashboard(request):
    users = User.objects.all()
    ctx = {'users':users}
    return render( request, 'admin/admindashboard.html', ctx)

def accounts(request):
    users = User.objects.all()
    userdata = UserData.objects.all()
    usercount = User.objects.all().count()
    ctx = {'users': users, 'usercount': usercount, 'userdata': userdata}
    return render(request, 'admin/accounts_page.html', ctx )

def standardfiles(request):
    standardfiles = Documents.objects.all()
    standardfilescount = Documents.objects.all().count()
    ctx = {'standardfiles': standardfiles, 'standardfilescount': standardfilescount}
    return render(request, 'admin/standardfilespage.html', ctx )

def standardsteps(request):
    standardsteps = Steps.objects.all()
    standardstepscount = Steps.objects.all().count()
    ctx = {'standardsteps': standardsteps, 'standardstepscount': standardstepscount}
    return render(request, 'admin/standardstepspage.html', ctx )

def standardworkflows(request):
    standardworkflow = ProjectTemplate.objects.all()
    standardworkflowcount = ProjectTemplate.objects.all().count()
    ctx = {'standardworkflows': standardworkflow, 'workflowcount': standardworkflowcount}
    return render(request, 'admin/standardworkflow.html', ctx )