from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
import json, re
from django.contrib.auth import login
from accountsapp.forms import RegisterForm
from accountsapp.models import *
from stepautomationapp.models import Steps, UserData

def guiee_signup(request, userdata_invite_code):
    if request.method == 'POST':
        userdata = UserData.objects.get(invite_code = userdata_invite_code)
        invitedby = userdata.userrelation
        print('-----invitedby-----', invitedby)
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
                user.is_staff = False
                user.is_active = True
                user.is_superuser = False
                user.save()
                login(request, user)
                guideeprofile =  GuideeProflie.objects.create(
                    user=user,
                    country='',
                    city='',
                    address='',
                    zipcode='',
                )
                guideeprofile.invited_by.add(invitedby)
                guideeprofile.save()
                return redirect('guidee/dsahboard')
        return HttpResponse(json.dumps({'status_msg': 'Ok', 'msg': 'Successfully Registered'}),
                                    content_type='application/json')

    else:
        userdata = UserData.objects.get(invite_code = userdata_invite_code)
        form = RegisterForm()
        return render(request, 'guidee/signup.html', {'form': form, 'userdata': userdata})

def guidee_dashboard(request):
    user = GuideeProflie.objects.get(user = request.user)
    guides = user.invited_by.filter(invited_by = user)
    workflows = []
    for item in guides:
        workflow =  item.projecttemplate_set.filter(user=item)
        for item in workflow:
            workflows.append(item)

    ctx = {'guides': guides, 'workflows': workflows}
    return render(request, 'guidee/guidee_dashboard.html', ctx)

def guidee_steps(request, project_template_id):
    steps = Steps.objects.filter(project_template__id = project_template_id)
    print('------------------', steps)
    ctx = {'steps': steps, }
    return render(request, 'guidee/steps.html', ctx)
