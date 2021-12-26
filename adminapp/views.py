from django.shortcuts import render
from stepautomationapp.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    profilepic = UserData.objects.get(userrelation = request.user)
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
        'totaluser': totaluser,
        'profilepic': profilepic.profilepic.url
        
    })

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser)
def accounts(request):
    profilepic = UserData.objects.get(userrelation = request.user)
    users = User.objects.all()
    userdata = UserData.objects.all()
    usercount = User.objects.all().count()
    ctx = {'users': users, 'usercount':
            usercount, 'userdata': userdata, 
            'profilepic': profilepic.profilepic.url }
    return render(request, 'admin/accounts_page.html', ctx )

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser)
def standardfiles(request):
    profilepic = UserData.objects.get(userrelation = request.user)
    standardfiles = Documents.objects.all().order_by('-file_add_date')
    standardfilescount = Documents.objects.all().count()
    ctx = {'standardfiles': standardfiles, 'standardfilescount': standardfilescount, 'profilepic': profilepic.profilepic.url }
    return render(request, 'admin/standardfilespage.html', ctx )

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser)
def standardsteps(request):
    profilepic = UserData.objects.get(userrelation = request.user)
    standardsteps = Steps.objects.all().order_by('-created_on')
    standardstepscount = Steps.objects.all().count()
    ctx = {'standardsteps': standardsteps, 'standardstepscount': standardstepscount, 'profilepic': profilepic.profilepic.url }
    return render(request, 'admin/standardstepspage.html', ctx )

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser)
def standardworkflows(request):
    profilepic = UserData.objects.get(userrelation = request.user)
    standardworkflow = ProjectTemplate.objects.all().order_by('-added_date')
    standardworkflowcount = ProjectTemplate.objects.all().count()
    ctx = {'standardworkflows': standardworkflow, 'workflowcount': standardworkflowcount, 'profilepic': profilepic.profilepic.url }
    return render(request, 'admin/standardworkflow.html', ctx )

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser)
def customerworkflows(request):
    profilepic = UserData.objects.get(userrelation = request.user)
    customerworkflow = CustomerWorkflow.objects.all().order_by('-added_date')
    customerworkflowcount = CustomerWorkflow.objects.all().count()
    ctx = {'customerworkflows': customerworkflow, 'customerworkflowcount': customerworkflowcount, 'profilepic': profilepic.profilepic.url }
    return render(request, 'admin/customerworkflow_page.html', ctx )

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser)
def customersteps(request):
    profilepic = UserData.objects.get(userrelation = request.user)
    customersteps = CustomerSteps.objects.all().order_by('-added_date')
    customerstepscount = CustomerSteps.objects.all().count()
    ctx = {'customersteps': customersteps, 'customerstepscount': customerstepscount, 'profilepic': profilepic.profilepic.url }
    return render(request, 'admin/customersteps.html', ctx )

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser)
def customers(request):
    profilepic = UserData.objects.get(userrelation = request.user)
    customers = Customers.objects.all().order_by('customer_name')
    customercount = Customers.objects.all().count()
    ctx = {'customers': customers, 'customercount': customercount, 'profilepic': profilepic.profilepic.url}
    return render(request, 'admin/customers_page.html', ctx )