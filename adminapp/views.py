from django.shortcuts import render
from stepautomationapp.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

@login_required(login_url='/')
def dashboard(request):
    labels = ['Admin', 'Guide', 'Guidee']
    admin = []
    guide = []
    guidee = []
    data = []
    queryset = User.objects.all()
    totaluser = User.objects.all().count()
    for user in queryset:
            if user.is_superuser:
                admin.append(user.username)
            elif user.is_staff: 
                guide.append(user.username)
            else:
                guidee.append(user.username)

    data.append(len(admin)), data.append(len(guide)), data.append(len(guidee))

    return render(request, 'admin/admindashboard.html', {
        'userlabels': labels,
        'userdata': data,
        'totaluser': totaluser
        
    })

@login_required(login_url='/')
def accounts(request):
    users = User.objects.all()
    userdata = UserData.objects.all()
    usercount = User.objects.all().count()
    ctx = {'users': users, 'usercount': usercount, 'userdata': userdata}
    return render(request, 'admin/accounts_page.html', ctx )

@login_required(login_url='/')
def standardfiles(request):
    standardfiles = Documents.objects.all().order_by('-file_add_date')
    standardfilescount = Documents.objects.all().count()
    ctx = {'standardfiles': standardfiles, 'standardfilescount': standardfilescount}
    return render(request, 'admin/standardfilespage.html', ctx )

@login_required(login_url='/')
def standardsteps(request):
    standardsteps = Steps.objects.all().order_by('-created_on')
    standardstepscount = Steps.objects.all().count()
    ctx = {'standardsteps': standardsteps, 'standardstepscount': standardstepscount}
    return render(request, 'admin/standardstepspage.html', ctx )

@login_required(login_url='/')
def standardworkflows(request):
    standardworkflow = ProjectTemplate.objects.all().order_by('-added_date')
    standardworkflowcount = ProjectTemplate.objects.all().count()
    ctx = {'standardworkflows': standardworkflow, 'workflowcount': standardworkflowcount}
    return render(request, 'admin/standardworkflow.html', ctx )

@login_required(login_url='/')
def customerworkflows(request):
    customerworkflow = CustomerWorkflow.objects.all().order_by('-added_date')
    customerworkflowcount = CustomerWorkflow.objects.all().count()
    ctx = {'customerworkflows': customerworkflow, 'customerworkflowcount': customerworkflowcount}
    return render(request, 'admin/customerworkflow_page.html', ctx )

@login_required(login_url='/')
def customersteps(request):
    customersteps = CustomerSteps.objects.all().order_by('-added_date')
    customerstepscount = CustomerSteps.objects.all().count()
    ctx = {'customersteps': customersteps, 'customerstepscount': customerstepscount}
    return render(request, 'admin/customersteps.html', ctx )

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser)
def customers(request):
    customers = Customers.objects.all().order_by('customer_name')
    customercount = Customers.objects.all().count()
    ctx = {'customers': customers, 'customercount': customercount}
    return render(request, 'admin/customers_page.html', ctx )