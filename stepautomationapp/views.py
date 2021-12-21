from os import error
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To

from .models import CustomerSteps, CustomerWorkflow, ProjectTemplate, UserData, UserFiles, Steps, Documents, Customers
from .models import Country
from userforms.models import UserForms
from .forms import CustomerStepsform, CustomerWorkflowForm, ProjectTemplateForm, Stepsform, DocumentsForm, CustomersForm


# landing page
def index(request):
    # if user is authenticated it will redirect to dashboard
    if request.user.is_authenticated and request.user.is_superuser :
        return redirect('adminuser/dashboard')
    elif request.user.is_authenticated :
        return redirect('/dashboard')
    else:
        return render(
            request,
            'demo-web-studio.html',
            {}
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
        username = request.POST.get('username')
        password = request.POST.get('password')
        keepsignin = request.POST.get('keepsignin')
        print(keepsignin)
        try:
            users = User.objects.get(email=username)
            if check_password(password, users.password):
                login(request, users)
                return HttpResponse(json.dumps({'status_msg': 'Ok'}),
                                    content_type='application/json')
            else:
                return HttpResponse(json.dumps({'status_msg': 'NotOk', 'msg': 'Invalid Username or Password'}),
                                    content_type='application/json')
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'status_msg': 'NotOk', 'msg': 'Invalid Username or Password'}),
                                content_type='application/json')


# creating new user
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            # if email already exists it will display error message
            usersemail = User.objects.get(email=email)
            return HttpResponse(json.dumps({'status_msg': 'NotOk', 'msg': 'User or Email Already Exists'}),
                                content_type='application/json')
        except User.DoesNotExist:
            # if emails doesn't exists it will create the user and redirect to users dashboard
            user = User.objects.create_user(
                username=email,
                password=password,
                email=email,
            )
            user.is_staff = False
            user.is_superuser = False
            user.save()
            login(request, user)
            return HttpResponse(json.dumps({'status_msg': 'Ok', 'msg': 'Successfully Registered'}),
                                content_type='application/json')


@login_required(login_url='/')
def dashboard(request):
    userdetails = User.objects.get(username=request.user)
    countries = Country.objects.all()
    try:
        # if user updated his profile picture or data
        userdata = UserData.objects.get(userrelation=userdetails)
        print(userdata.profilepic)
        print(userdata.country)
        return render(
            request,
            'account-profile.html',
            {
                'logged': True,
                'username': userdetails.username,
                'email': userdetails.email,
                'first_name': userdetails.first_name,
                'last_name': userdetails.last_name,
                'address': userdata.address,
                'zipcode': userdata.zipcode,
                'country': userdata.country,
                'city': userdata.city,
                'profilepic': 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic),
                'countries': countries,
            }
        )
    except UserData.DoesNotExist:
        return render(
            request,
            'account-profile.html',
            {
                'logged': True,
                'username': userdetails.username,
                'email': userdetails.email,
                'first_name': userdetails.first_name,
                'last_name': userdetails.last_name,
                'address': '',
                'zipcode': '',
                'country': False,
                'city': False,
                'profilepic': 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png',
                'countries': countries
            }
        )


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
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user.id)
        userdata.country = request.POST.get('country')
        userdata.city = request.POST.get('city')
        userdata.address = request.POST.get('address')
        userdata.zipcode = request.POST.get('zipcode')
        userdata.save()
    except UserData.DoesNotExist:
        userdata = UserData.objects.create(
            userrelation=user,
            country=request.POST.get('country'),
            city=request.POST.get('city'),
            address=request.POST.get('address'),
            zipcode=request.POST.get('zipcode')
        )
        userdata.save()
    return redirect('/account-profile')


# for updating the profile picture of the user
@login_required(login_url='/')
def updateProfilePic(request):
    user = User.objects.get(username=request.user)
    try:

        userdetails = UserData.objects.get(userrelation=user.id)
        userdetails.profilepic = request.FILES.get('profilepic')
        userdetails.save()
        return redirect('/account-profile')
    except UserData.DoesNotExist:
        userdetails = UserData.objects.create(
            userrelation=user,
            profilepic=request.FILES.get('profilepic'),
            address='',
            country='',
            city='',
            zipcode=''
        )
        userdetails.save()
        return redirect('/account-profile')


# to create steps of the user
@login_required(login_url='/')
def handleStepFiles(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
        print(profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
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
def get_project_details(request, projectName):
    userdetails = User.objects.get(username=request.user)
    data = UserFiles.objects.get(user=userdetails, projectName=projectName)
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
                'profilepic': 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic),
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
                'profilepic': 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png',
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
def create_steps(request, project_template_pk):
    user = User.objects.get(username=request.user)
    project_template = ProjectTemplate.objects.get(pk=project_template_pk)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
        print(profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
        username = request.user
    if request.method == 'POST':
        form = Stepsform(request.POST, request.FILES)
        if form.is_valid():
            step = form.save(commit=False)
            step.user = request.user
            step.project_template = project_template
            step.save()
            form = Stepsform()
            return redirect(
                    f'/displaysteps/{project_template_pk}/'
                )
           
        else:
            form = Stepsform()
            return render(
                request,
                'create_steps.html',
                {
                    'username': username,
                    'profilepic': profilepic,
                    'form': form
                }
            )
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

def edit_step(request, steps_pk, project_template_pk):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
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



def delete_steps(request, project_template_pk, steps_pk):
    steps = Steps.objects.get(id = steps_pk, project_template_id = project_template_pk).delete()
    return redirect(f'/displaysteps/{project_template_pk}')


@login_required(login_url='/')
def display_steps(request, project_template_pk ):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
        username = request.user
    steps = Steps.objects.filter(project_template_id = project_template_pk)
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
def dashboard_details(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
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
def template_details(request):
    user = User.objects.get(username=request.user)
    project_template = ProjectTemplate.objects.filter(user = user)
    form = ProjectTemplateForm()
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
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
def documents_details(request):
    user = User.objects.get(username=request.user)
    form = DocumentsForm()
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
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
def clients_details(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
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
def cases_details(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
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
def project_details(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
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
def customers_details(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
        username = request.user
    customers = Customers.objects.filter(user=request.user.username)
    return render(
        request,
        'customers.html',
        {
            'username': username,
            'profilepic': profilepic,
            'customers': customers
        }
    )


@login_required(login_url='/')
def edit_customer(request, customer_id):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
        username = request.user
    customer = Customers.objects.get(id=customer_id)
    if request.method == 'POST':
        form = CustomersForm(instance=customer, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/editcustomer/' + str(customer_id))
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
def delete_customer(request, customer_id):
    Customers.objects.get(id=customer_id).delete()
    return redirect('/customers')


# user to add the documents
@login_required(login_url='/')
def create_document(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
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
def create_customer(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
        username = request.user
    if request.method == 'POST':
        form = CustomersForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user.username
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
def create_project_template(request):
    user = User.objects.get(username=request.user)
    # project_template = ProjectTemplate.objects.get(pk = project_template_pk)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
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


def edit_project_template(request, project_template_pk):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
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

    

def delete_project_template(request, project_template_pk):
    ProjectTemplate.objects.get(pk=project_template_pk).delete()
    return redirect('/workflows')


def edit_document(request, documents_pk):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
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



def delete_document(request, documents_pk):
    Documents.objects.get(pk=documents_pk).delete()
    return redirect('/documents')


@login_required(login_url='/')
def create_customersteps(request, customerworkflow_pk):
    user = User.objects.get(username=request.user)
    customerworkflow = CustomerWorkflow.objects.get(pk=customerworkflow_pk)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
        print(profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
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

def edit_customerstep(request, customersteps_pk, customerworkflow_pk):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
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


def delete_customerstep(request, customersteps_pk, customerworkflow_pk):
    steps = CustomerSteps.objects.get(id = customersteps_pk, customerworkflow_id = customerworkflow_pk).delete()
    return redirect(f'/customerworkflowsteps/{customerworkflow_pk}/')


@login_required(login_url='/')
def display_customerstep(request, customerworkflow_pk ):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
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
def create_customerworkflow(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
        username = request.user

    if request.method == 'POST':
        form = CustomerWorkflowForm(request.POST)
        if form.is_valid():
            customerworkflow = form.save(commit=False)
            customerworkflow.user = request.user
            customerworkflow.save()
            return redirect(
                    '/customerworkflows'
                )
        else:
            form = CustomerWorkflowForm()
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
        form = CustomerWorkflowForm()
        return render(
            request,
            'create_customerworkflow.html',
            {
                'username': username,
                'profilepic': profilepic,
                'form': form
            }
        )


def edit_customerworkflow(request, customerworkflow_pk):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
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
def customerworkflow_details(request):
    user = User.objects.get(username=request.user)
    customerworkflow = CustomerWorkflow.objects.filter(user = user)
    form = CustomerWorkflowForm
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
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



def delete_customerworkflow(request, customerworkflow_pk):
    CustomerWorkflow.objects.get(pk=customerworkflow_pk).delete()
    return redirect('/customerworkflows')