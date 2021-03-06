from os import error
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.authtoken.models import Token
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To
import re
from .models import *
from .models import Country
from userforms.models import UserForms
from .forms import *
from accountsapp.forms import *


# landing page
def index(request):
    loginform = LoginForm()
    registerform = RegisterForm()
    # if user is authenticated it will redirect to dashboard
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('/adminuser/dashboard')
    elif request.user.is_authenticated and request.user.is_staff:
        return redirect('/dashboard')
    elif request.user.is_authenticated and not request.user.is_staff and not request.user.is_superuser:
        return redirect('guidee/dashboard')
    else:
        return render(
            request,
            'demo-web-studio.html',
            {'loginform': loginform, 'registerform': registerform}
        )


'''def handle_redirect(request, template):
    return render(
        request,
        template + '.html',
        {}
    )'''

# delete the user account
@login_required(login_url='/')
def delete_account(request):
    user = User.objects.get(username=request.user)
    UserForms.objects.filter(form_user=request.user.username).delete()
    UserFiles.objects.filter(user=user).delete()
    logout(request)
    user.delete()
    return redirect('/')


# check the user is authenticated or not
def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid(): 
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                if user.is_superuser:
                    return redirect('/adminuser/dashboard')
                elif user.is_staff: 
                    return redirect('/dashboard')
                else:
                    return redirect('guidee/dashboard/')
                
            else:
                return HttpResponse(json.dumps({'status_msg': 'NotOk', 'msg': 'Invalid Email and Password'}),
                                content_type='application/json')
        else :
            return HttpResponse(json.dumps({'status_msg': 'NotOk', 'msg': 'Invalid Deatils'}),
                                    content_type='application/json')
    else:
        form = LoginForm()
        ctx = {'form' : form}
        return render(request, 'accounts/login.html', ctx)
    

# creating new user
def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                # if email already exists it will display error message
                usersemail = User.objects.get(email=email)
                return HttpResponse(json.dumps({'status_msg': 'NotOk', 'msg': 'User or Email Already Exists'}),
                                    content_type='application/json')
            except User.DoesNotExist:
                res = re.search(r'@[\w-]+\.[\w.-]+', email)
                res = res.group(0)
                username = email.replace(res, '')
                user = form.save(commit=False)
                user.username = username
                user.is_staff = True
                user.is_active = True
                user.is_superuser = False
                user.save()
                login(request, user)
                return redirect('/dashboard')
        else :
            return HttpResponse(json.dumps({'status_msg': 'NotOk', 'msg': 'Invalid Deatils'}),
                                    content_type='application/json')

@login_required(login_url='/')
def dashboard(request):
    return render(request, 'dashboard.html')


# to create the dependent dropdown for the city and states
# this will return cities dependent on their countries
@permission_classes([permissions.AllowAny])
def getCities(request):
    sname = request.GET['countrydata']
    results = []
    answer = str(sname)
    selected_country = Country.objects.get(country=answer)
    cities = selected_country.city_set.all()
    for city in cities:
        results.append({'name': city.city})
    return HttpResponse(json.dumps(results), content_type='application/json')


# for updating the user profile
@login_required(login_url='/')
def updateProfile(request):
    userdetails = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=userdetails)
        username = userdetails.username
        profilepic = userdata.profilepic
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    try:
        user_data = UserData.objects.get(userrelation=userdetails)
        if request.method == 'POST':
            form = UserDataForm(request.POST or None, request.FILES, instance=user_data)
            if form.is_valid():
                form.save()
                return redirect(f'/account-profile')
            else: 
                return redirect(f'/account-profile')

        else :
            form = UserDataForm(request.POST or None, instance=user_data)
            return render(
                request,
                'account-profile.html',
                {
                    'userdataform': form,
                    'profilepic': profilepic
,
                    
                }
        )
    except UserData.DoesNotExist:
        if request.method == 'POST':
            form = UserDataForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                form.userrelation = request.user
                form.save()
            else:
                return redirect('/account-profile')
        else:
            form = UserDataForm()
            return render(
                request,
                'account-profile.html',
                {
                    'userdataform': form,
                    'profilepic': profilepic
                }
            )


# for updating the profile picture of the user



# to create steps of the user
@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def handleStepFiles(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
        print(profilepic)
    except UserData.DoesNotExist:
        profilepic = '../static/assets/images/profilepic.png'
        username = request.user
    userdata = UserFiles.objects.filter(user=user)
    if userdata.count() == 0:
        has_files = False
    else:
        has_files = True
    print(has_files)
    if request.method == 'POST':
        projectName = request.POST.get('projectName')
        try:
            # check if the project name already exist in that user account
            project = UserFiles.objects.get(user=user, projectName=projectName)
            return render(
                request,
                'add_files.html',
                {
                    'username': user.username,
                    'profilepic': profilepic,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'has_files': has_files,
                    'userdata': userdata,
                    'fail': 'Project Name Already Exists'
                }
            )
        except UserFiles.DoesNotExist:
            # if project name doesn't exists it will create steps for the user
            customerName = request.POST.get('customerName')
            projectDescription = request.POST.get('projectDescription')
            userfile = UserFiles.objects.create(
                user=user,
                projectName=projectName,
                customerName=customerName,
                description=projectDescription,
                userFile=request.FILES.get('userfile')
            )
            userfile.save()
            return render(
                request,
                'add_files.html',
                {
                    'username': user.username,
                    'profilepic': profilepic,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'has_files': has_files,
                    'userdata': userdata,
                    'success': 'Updated Information Successfully'
                }
            )
    else:
        return render(
            request,
            'add_files.html',
            {
                'username': username,
                'profilepic': profilepic,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'has_files': has_files,
                'userdata': userdata,
            }
        )


# to get the details of the project based on their project name
@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def get_project_details(request, projectName):
    userdetails = User.objects.get(username=request.user)
    data = UserFiles.objects.get(user=userdetails, projectName=projectName)
    profilepic = UserData.objects.get(userrelation = request.user)

    try:
        userdata = UserData.objects.get(userrelation=userdetails)
        return render(
            request,
            'project_details.html',
            {
                'username': userdetails.username,
                'email': userdetails.email,
                'first_name': userdetails.first_name,
                'last_name': userdetails.last_name,
                'data': data,
                'profilepic': profilepic.profilepic.url,
            }
        )
    except UserData.DoesNotExist:
        return render(
            request,
            'project_details.html',
            {
                'username': userdetails.username,
                'email': userdetails.email,
                'first_name': userdetails.first_name,
                'last_name': userdetails.last_name,
                'data': data,
                'profilepic': profilepic.profilepic.url,
            }
        )


# to send the et password link to the user registered email
def forgetPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            # check the user entered email is in records
            user = User.objects.get(email=email)
            try:
                authToken = Token.objects.get(user_id=user.id)
                return render(
                    request,
                    'password-recovery.html',
                    {
                        'fail': 'Email Already Sent to ' + email
                    }
                )
            except Token.DoesNotExist:
                # it will generate a token to identify the user
                token_generation = Token.objects.create(user_id=user.id)
                token_generation.save()
                authToken = Token.objects.get(user_id=user.id)
                authKey = authToken.key
                try:
                    sg = SendGridAPIClient(settings.SENDGRID_EMAIL_API)
                    message = Mail(
                        from_email=Email(settings.FROM_EMAIL),
                        to_emails=To(email),
                        subject='Password Reset For StepSaas Application',
                        html_content='<a href="https://stepsaasautomation.herokuapp.com/update-password/' + authKey + '"><input '
                                                                                                                      'type="submit" '
                                                                                                                      'value="Reset '
                                                                                                                      'Password"></a> '
                    )
                    print("Message")
                    response = sg.send(message)
                    print(response.status_code)
                    return render(
                        request,
                        'password-recovery.html',
                        {
                            'success': 'Password reset link sent to  ' + email
                        }
                    )
                except Exception:
                    return render(
                        request,
                        'password-recovery.html',
                        {
                            'fail': 'An Error Occurred '
                        }
                    )
        except User.DoesNotExist:
            return render(
                request,
                'password-recovery.html',
                {
                    'fail': 'Email Does not exists'
                }
            )
    else:
        return render(
            request,
            'password-recovery.html'
        )


# to update the password from the forget password link
def update_password(request, token):
    try:
        user_token = Token.objects.get(key=token)
        if request.method == 'POST':
            password = request.POST.get('password')
            cpassword = request.POST.get('cpassword')
            if password == cpassword:
                print(user_token)
                print(user_token.user)
                user = User.objects.get(username=user_token.user)
                user.set_password(password)
                user.save()
                user_token.delete()
                return render(
                    request,
                    'update_password.html',
                    {
                        'success': 'Password Updated',
                        'expires': False
                    }
                )
            else:
                return render(
                    request,
                    'update_password.html',
                    {
                        'fail': 'Password not Matched',
                        'expires': False
                    }
                )
        else:
            return render(
                request,
                'update_password.html',
                {'expires': False}
            )
    except Token.DoesNotExist:
        return render(
            request,
            'update_password.html',
            {'expires': True}
        )


@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def create_steps(request, project_template_pk):
    user = User.objects.get(username=request.user)
    project_template = ProjectTemplate.objects.get(pk=project_template_pk)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    if request.method == 'POST':
        form = Stepsform(request.POST, request.FILES)
        if form.is_valid():
            step = form.save(commit=False)
            step.user = request.user
            step.project_template = project_template
            step.save()
            form = Stepsform()
            return redirect(f'/displaysteps/{project_template_pk}/')
        else:
            return HttpResponse("The Step number you're trying is already in use, Please try using different step number.")
    else:
        form = Stepsform()
        return render(
            request,
            'create_steps.html',
            {
                'username': username,
                'profilepic': profilepic,
                'project_template' : project_template,
                'form': form
            }
        )

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def edit_step(request, steps_pk, project_template_pk):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    project_template = ProjectTemplate.objects.get(id = project_template_pk)
    step = Steps.objects.get(id=steps_pk, project_template__id = project_template_pk)
    if request.method == 'POST':
        form = Stepsform(request.POST or None, instance=step)
        if form.is_valid():
            form.save()
            return redirect(f'/displaysteps/{project_template_pk}')
        else: 
            return redirect(f'/displaysteps/{project_template_pk}')

    else:
        form = Stepsform(request.POST or None, instance = step)
        ctx = {'form': form, 'username': username, 'profilepic': profilepic, 'step': step, 'project_template': project_template}
        return render(request, 'edit_steps.html', ctx)


@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def delete_steps(request, project_template_pk, steps_pk):
    steps = Steps.objects.get(id = steps_pk, project_template_id = project_template_pk).delete()
    return redirect(f'/displaysteps/{project_template_pk}')


@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def display_steps(request, project_template_pk ):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    steps = Steps.objects.filter(project_template_id = project_template_pk).order_by('count')
    project_template = ProjectTemplate.objects.get(id = project_template_pk)
    form = Stepsform()
    
    return render(
        request,
        'display_steps.html',
        {
            'username': username,
            'profilepic': profilepic,
            'steps': steps,
            'project_template' : project_template,
            'createform': form,
        }
    )


@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def dashboard_details(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    return render(
        request,
        'dashboard.html',
        {
            'username': username,
            'profilepic': profilepic,
        }
    )



@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def template_details(request):
    user = User.objects.get(username=request.user)
    project_template = ProjectTemplate.objects.filter(user = user)
    form = ProjectTemplateForm()
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    return render(
        request,
        'templates_page.html',
        {
            'username': username,
            'profilepic': profilepic,
            'form': form,
            'project_template': project_template,
        }
    )



# to display the documents of current user
@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def documents_details(request):
    user = User.objects.get(username=request.user)
    form = DocumentsForm()
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    documents = Documents.objects.filter(user=request.user.username)
    return render(
        request,
        'documents_page.html',
        {
            'username': username,
            'profilepic': profilepic,
            'documents': documents,
            'createform': form
        }
    )


@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def clients_details(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    return render(
        request,
        'clients_page.html',
        {
            'username': username,
            'profilepic': profilepic,
        }
    )


@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def cases_details(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    return render(
        request,
        'cases_page.html',
        {
            'username': username,
            'profilepic': profilepic,
        }
    )


@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def project_details(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    return render(
        request,
        'projects.html',
        {
            'username': username,
            'profilepic': profilepic,
        }
    )


@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def customers_details(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    customers = Customers.objects.filter(user=request.user.username)
    form = CustomersForm()
    return render(
        request,
        'customers.html',
        {
            'username': username,
            'profilepic': profilepic,
            'customers': customers,
            'form': form
        }
    )


@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def edit_customer(request, customer_id):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    customer = Customers.objects.get(id=customer_id)
    if request.method == 'POST':
        form = CustomersForm(instance=customer, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/customers')
        else:
            return render(
                request,
                'edit_customer.html',
                {
                    'username': username,
                    'profilepic': profilepic,
                    'form': form
                }
            )
    else:
        form = CustomersForm(instance=customer)
        return render(
            request,
            'edit_customer.html',
            {
                'username': username,
                'profilepic': profilepic,
                'form': form
            }
        )


@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def delete_customer(request, customer_id):
    Customers.objects.get(id=customer_id).delete()
    return redirect('/customers')


# user to add the documents
@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def create_document(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    if request.method == 'POST':
        form = DocumentsForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            return redirect('/documents')
        else:
            return render(
                request,
                'create_documents.html',
                {
                    'username': username,
                    'profilepic': profilepic,
                    'createform': form
                }
            )
    else:
        form = DocumentsForm(initial={'apostille': 'No', 'notarize': 'No'})
        return render(
            request,
            'create_documents.html',
            {
                'username': username,
                'profilepic': profilepic,
                'createform': form
            }
        )


@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def create_customer(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    if request.method == 'POST':
        form = CustomersForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()
            return redirect('/customers')
        else:
            return render(
                request,
                'create_customer.html',
                {
                    'username': username,
                    'profilepic': profilepic,
                    'form': form
                }
            )
    else:
        form = CustomersForm()
        return render(
            request,
            'create_customer.html',
            {
                'username': username,
                'profilepic': profilepic,
                'form': form
            }
        )


def aboutus(request):
    return render(
        request,
        'about.html',
        {}
    )


def contactus(request):
    return render(
        request,
        'contacts-v3.html',
        {}
    )


@login_required(login_url='/')
def user_logout(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def create_project_template(request):
    user = User.objects.get(username=request.user)
    # project_template = ProjectTemplate.objects.get(pk = project_template_pk)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user

    if request.method == 'POST':
        form = ProjectTemplateForm(request.POST)
        if form.is_valid():
            project_template = form.save(commit=False)
            project_template.user = request.user
            project_template.save()
            form = ProjectTemplateForm()
            return redirect(
                    '/workflows'
                )
        else:
            form = ProjectTemplateForm()
            return render(
                request,
                'create_project_template.html',
                {
                    'username': username,
                    'profilepic': profilepic,
                    'form': form
                }
            )
    else:
        form = ProjectTemplateForm()
        return render(
            request,
            'create_project_template.html',
            {
                'username': username,
                'profilepic': profilepic,
                'form': form
            }
        )

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def edit_project_template(request, project_template_pk):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user

    if request.method == 'POST':
        project_template = ProjectTemplate.objects.get(id = project_template_pk)
        form = ProjectTemplateForm(request.POST or None, instance = project_template)
        if form.is_valid():
            form.save()
            return redirect('/workflows')
        else: 
            return redirect('/workflows')

    else:
        project_template = ProjectTemplate.objects.get(id = project_template_pk)
        form = ProjectTemplateForm(request.POST or None, instance = project_template)
        ctx = {'form': form, 'username': username, 'profilepic': profilepic }
        return render(request, 'edit_project_template.html', ctx)

    
@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def delete_project_template(request, project_template_pk):
    ProjectTemplate.objects.get(pk=project_template_pk).delete()
    return redirect('/workflows')

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def edit_document(request, documents_pk):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user

    document = Documents.objects.get(id=documents_pk)
    if request.method == 'POST':
        form = DocumentsForm(request.POST or None, instance=document)
        if form.is_valid():
            form.save()
            return redirect('/documents')
        else: 
            return redirect('/documents')

    else:
        form = DocumentsForm(request.POST or None, instance = document)
        ctx = {'form': form, 'username': username, 'profilepic': profilepic}
        return render(request, 'edit_document.html', ctx)


@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def delete_document(request, documents_pk):
    Documents.objects.get(pk=documents_pk).delete()
    return redirect('/documents')


@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def create_customersteps(request, customerworkflow_pk):
    user = User.objects.get(username=request.user)
    customerworkflow = CustomerWorkflow.objects.get(pk=customerworkflow_pk)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
        print(profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    if request.method == 'POST':
        form = CustomerStepsform(request.POST, request.FILES)
        if form.is_valid():
            step = form.save(commit=False)
            step.user = request.user
            step.customerworkflow = customerworkflow
            step.save()
            form = CustomerStepsform()
            return redirect(
                    f'/customerworkflowsteps/{customerworkflow_pk}/'
                )
           
        else:
            form = CustomerStepsform()
            return render(
                request,
                'create_customersteps.html',
                {
                    'username': username,
                    'profilepic': profilepic,
                    'form': form
                }
            )
    else:
        form = CustomerStepsform()
        return render(
            request,
            'create_customersteps.html',
            {
                'username': username,
                'profilepic': profilepic,
                'customerworkflow' : customerworkflow,
                'form': form
            }
        )

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def edit_customerstep(request, customersteps_pk, customerworkflow_pk):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user

    customerworkflow = CustomerWorkflow.objects.get(id = customerworkflow_pk)
    step = CustomerSteps.objects.get(id=customersteps_pk, customerworkflow_id = customerworkflow_pk)
    if request.method == 'POST':
        form = CustomerStepsform(request.POST or None, instance=step)
        if form.is_valid():
            form.save()
            return redirect(f'/customerworkflowsteps/{customerworkflow_pk}/')
        else: 
            return redirect(f'/customerworkflowsteps/{customerworkflow_pk}/')

    else:
        form = CustomerStepsform(request.POST or None, instance = step)
        ctx = {'form': form, 'username': username, 'profilepic': profilepic, 'step': step, 'customerworkflow': customerworkflow}
        return render(request, 'edit_customersteps.html', ctx)

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def delete_customerstep(request, customersteps_pk, customerworkflow_pk):
    steps = CustomerSteps.objects.get(id = customersteps_pk, customerworkflow_id = customerworkflow_pk).delete()
    return redirect(f'/customerworkflowsteps/{customerworkflow_pk}/')


@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def display_customerstep(request, customerworkflow_pk ):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    steps = CustomerSteps.objects.filter(customerworkflow_id = customerworkflow_pk)
    customerworkflow = CustomerWorkflow.objects.get(id = customerworkflow_pk)
    form = CustomerStepsform()
    
    return render(
        request,
        'display_customersteps.html',
        {
            'username': username,
            'profilepic': profilepic,
            'steps': steps,
            'customerworkflow' : customerworkflow,
            'createform': form,
        }
    )


@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def create_customerworkflow(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user

    if request.method == 'POST':
        form = CustomerWorkflowForm( request.user, request.POST)
        if form.is_valid():
            customerworkflow = form.save(commit=False)
            customerworkflow.user = request.user
            customerworkflow.save()
            return redirect(
                    '/customerworkflows'
                )
        else:
            form = CustomerWorkflowForm(request.user)
            return render(
                request,
                'create_customerworkflow.html',
                {
                    'username': username,
                    'profilepic': profilepic,
                    'form': form
                }
            )
    else:
        form = CustomerWorkflowForm(request.user)
        return render(
            request,
            'create_customerworkflow.html',
            {
                'username': username,
                'profilepic': profilepic,
                'form': form
            }
        )

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def edit_customerworkflow(request, customerworkflow_pk):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    if request.method == 'POST':
        customerworkflow = CustomerWorkflow.objects.get(id = customerworkflow_pk)
        form = CustomerWorkflowForm(request.POST or None, instance = customerworkflow)
        if form.is_valid():
            form.save()
            return redirect('/customerworkflows')
        else: 
            return redirect('/customerworkflows')

    else:
        customerworkflow = CustomerWorkflow.objects.get(id = customerworkflow_pk)
        form = CustomerWorkflowForm(request.POST or None, instance = customerworkflow)
        ctx = {'form': form, 'username': username, 'profilepic': profilepic }
        return render(request, 'edit_customerworkflow.html', ctx)


@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def customerworkflow_details(request):
    user = User.objects.get(username=request.user)
    customerworkflow = CustomerWorkflow.objects.filter(user = user)
    form = CustomerWorkflowForm(request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = userdata.profilepic.url
    except UserData.DoesNotExist:
        profilepic = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1214428300?k=20&m=1214428300&s=170667a&w=0&h=NPyJe8rXdOnLZDSSCdLvLWOtIeC9HjbWFIx8wg5nIks='
        username = request.user
    return render(
        request,
        'customerworkflow_detail.html',
        {
            'username': username,
            'profilepic': profilepic,
            'form': form,
            'customerworkflow': customerworkflow,
        }
    ) 


@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def delete_customerworkflow(request, customerworkflow_pk):
    CustomerWorkflow.objects.get(pk=customerworkflow_pk).delete()
    return redirect('/customerworkflows')