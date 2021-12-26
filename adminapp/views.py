from django.shortcuts import render
from stepautomationapp.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
        print(profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
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
        'profilepic': profilepic
        
    })

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser)
def accounts(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
        print(profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    users = User.objects.all()
    userdata = UserData.objects.all()
    usercount = User.objects.all().count()
    ctx = {'users': users, 'usercount':
            usercount, 'userdata': userdata, 
            'profilepic': profilepic }
    return render(request, 'admin/accounts_page.html', ctx )

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser)
def standardfiles(request):
    try:
        userdata = UserData.objects.get(userrelation=request.user)
        username = request.user.username
        profilepic = userdata.profilepic.url
        print(profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    standardfiles = Documents.objects.all().order_by('-file_add_date')
    standardfilescount = Documents.objects.all().count()
    ctx = {'standardfiles': standardfiles, 'standardfilescount': standardfilescount, 'profilepic': profilepic }
    return render(request, 'admin/standardfilespage.html', ctx )

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser)
def standardsteps(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
        print(profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    standardsteps = Steps.objects.all().order_by('-created_on')
    standardstepscount = Steps.objects.all().count()
    ctx = {'standardsteps': standardsteps, 'standardstepscount': standardstepscount, 'profilepic': profilepic }
    return render(request, 'admin/standardstepspage.html', ctx )

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser)
def standardworkflows(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
        print(profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    standardworkflow = ProjectTemplate.objects.all().order_by('-added_date')
    standardworkflowcount = ProjectTemplate.objects.all().count()
    ctx = {'standardworkflows': standardworkflow, 'workflowcount': standardworkflowcount, 'profilepic': profilepic }
    return render(request, 'admin/standardworkflow.html', ctx )

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser)
def customerworkflows(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
        print(profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    customerworkflow = CustomerWorkflow.objects.all().order_by('-added_date')
    customerworkflowcount = CustomerWorkflow.objects.all().count()
    ctx = {'customerworkflows': customerworkflow, 'customerworkflowcount': customerworkflowcount, 'profilepic': profilepic }
    return render(request, 'admin/customerworkflow_page.html', ctx )

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser)
def customersteps(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
        print(profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    customersteps = CustomerSteps.objects.all().order_by('-added_date')
    customerstepscount = CustomerSteps.objects.all().count()
    ctx = {'customersteps': customersteps, 'customerstepscount': customerstepscount, 'profilepic': profilepic }
    return render(request, 'admin/customersteps.html', ctx )

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser)
def customers(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
        print(profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    customers = Customers.objects.all().order_by('customer_name')
    customercount = Customers.objects.all().count()
    ctx = {'customers': customers, 'customercount': customercount, 'profilepic': profilepic}
    return render(request, 'admin/customers_page.html', ctx )