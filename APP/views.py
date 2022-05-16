from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings
from django.template import loader 
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.db import IntegrityError
from jira import JIRA, JIRAError
from APP.models import *

def Home(request):
    return render(request, "home.html")

def SignIn(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active == 1:
                user = ActivationTokens.objects.get(username=request.POST['username'])
                if UserJiraCredentials.objects.filter(token=user.token).exists():
                    U = urlsafe_base64_encode(force_bytes(user.username))
                    return redirect('signin/jiradirectaccess/'+U)
                else:
                    AT = ActivationTokens.objects.get(id=user.pk).token
                    return redirect('signin/jiraaccess/'+AT)
            else:
                msg = "Please activate your account first"
                context = {'message': msg}
                return render(request, "signin.html", context) 
        else:
            msg = "Sorry ... username or password is incorrect"
            context = {'message': msg}
            return render(request, "signin.html", context)         
    else:        
        return render(request, "signin.html") 

def SignUp(request):
    if request.method == 'POST':    
        if User.objects.filter(username=request.POST['username']).exists():
            msg = "Sorry ... username already taken"
            context = {'message': msg}
            return render(request, "signup.html", context)
        elif User.objects.filter(email=request.POST['email']).exists():
            msg = "Sorry ... email already taken"
            context = {'message': msg}
            return render(request, "signup.html", context)      
        else:       
            User.objects.create(username=request.POST['username'], email=request.POST['email'], is_active=0)
            user = User.objects.get(username=request.POST['username'])
            user.set_password(request.POST['password'])
            user.save()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            user_token = default_token_generator.make_token(user)
            ActivationTokens.objects.create(username=user.username, token=user_token)
            email_message = loader.render_to_string('template1.html', {'username': request.POST['username'], 'uid': uid, 'token': user_token})          
            send_mail(subject='Activation Account',
                      message=email_message, 
                      html_message=email_message, 
                      from_email=settings.EMAIL_HOST_USER, 
                      recipient_list=[user.email])
            msg = "Please check your email and activate your account"
            context = {'message': msg}
            return render(request, "signup.html", context)         
    else:
        return render(request, "signup.html")        

def ActivateAccount(request, uid, token):
    try:
        user = User.objects.get(id=urlsafe_base64_decode(uid).decode())
        user_activation_token = ActivationTokens.objects.get(id=urlsafe_base64_decode(uid).decode(), token=token) 
    except User.DoesNotExist or ActivationTokens.DoesNotExist:
        user = None    
    if user is not None:
        if user.is_active == 0:
            ResetPasswordTokens.objects.create(id=user.pk, token=default_token_generator.make_token(user))
            user.is_active = 1
            user.save()
            msg = "Your account has been successfully activated"
            context = {'message1': msg}
            return render(request, "success.html", context)  
        else:
            msg = "Your account is already activated"
            context = {'message2': msg}
            return render(request, "success.html", context)                                
    else:
        return render(request, "oops.html")        

def ForgotPassword(request):
    if request.method == 'POST':    
        if User.objects.filter(email=request.POST['email']).exists():
            user = User.objects.get(email=request.POST['email'])
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            user_reset_token = ResetPasswordTokens.objects.get(id=urlsafe_base64_decode(uid).decode()).token 
            email_message = loader.render_to_string('template2.html', {'username': user.username, 'uid': uid, 'token': user_reset_token})          
            send_mail(subject='Password Reset Request', 
                      message=email_message, 
                      html_message=email_message, 
                      from_email=settings.EMAIL_HOST_USER, 
                      recipient_list=[user.email])
            return render(request, "check.html")
        else:
            msg = "Sorry ... email doesn't exist"
            context = {'message': msg} 
            return render(request, "reset.html", context)
    else:
        return render(request, "reset.html")        

def ResetPassword(request, uid, token):
    try:
        user = User.objects.get(id=urlsafe_base64_decode(uid).decode(), is_active=1)
        user_reset_token = ResetPasswordTokens.objects.get(id=urlsafe_base64_decode(uid).decode(), token=token)
    except User.DoesNotExist or ResetPasswordTokens.DoesNotExist:
        user = None   
    if request.method == 'POST':
        if user is not None:
            if request.POST['password1'] == request.POST['password2']:
                user = User.objects.get(id=urlsafe_base64_decode(uid).decode(), is_active=1)
                user.set_password(request.POST['password1'])
                user.save()
                user_reset_token.token = default_token_generator.make_token(user)
                user_reset_token.save()
                msg = "Your password has been successfully changed"
                context = {'message3': msg}
                return render(request, "success.html", context)  
            else:
                msg = "Passwords are not the same"
                context = {'message': msg}
                return render(request, "change.html", context)                                       
        else:
            return render(request, "oops.html")                
    else:       
        return render(request, "change.html") 

def JiraDirectAccess(request, username):
    try:
        user = ActivationTokens.objects.get(username=urlsafe_base64_decode(username).decode())                
    except ActivationTokens.DoesNotExist:
        user = None
    if user is not None:
        user_credentials = UserJiraCredentials.objects.get(token=user.token)
        try: 
            jiraOptions = {'server': "https://"+str(user_credentials.project)+".atlassian.net"}
            jira = JIRA(options=jiraOptions, basic_auth=(user_credentials.email, user_credentials.jiratoken))
            projects = jira.projects()
            if len(projects) == 0:
                JiraIssues.objects.all().delete()
                msg = "There is no projects available"
                context = {'message': msg}
                return render(request, "signin.html", context)  
            else:
                JiraIssues.objects.all().delete()
                for prj in projects:
                    for issue in jira.search_issues(jql_str='project='+str(prj)):
                        try:
                            JiraIssues.objects.update_or_create(token=user_credentials.token,
                                                                project=prj,
                                                                issuetype=issue.fields.issuetype,
                                                                issuekey=issue.key,
                                                                issuesummuray=issue.fields.summary,
                                                                issuedescription=issue.fields.description,
                                                                issueassignee=issue.fields.assignee,
                                                                issuereporter=issue.fields.reporter,
                                                                issuepriority=issue.fields.priority,
                                                                issuestatus=issue.fields.status,
                                                                issueresolution=issue.fields.resolution,
                                                                issuecreated=issue.fields.created,
                                                                issueupdated=issue.fields.updated,
                                                                issuedue=issue.fields.duedate)    
                        except JIRAError or IntegrityError:
                            pass
                LOI = JiraIssues.objects.all().order_by('issueupdated')
                context = {'list': LOI.reverse(), 'project': user_credentials.project}      
                return render(request, "jiraissues.html", context) 
        except JIRAError:
            return render(request, "oops.html")
    else:
        return render(request, "oops.html")         

def JiraAccess(request, token):
    if request.method == 'POST':
        try: 
            jiraOptions = {'server': "https://"+request.POST['project']+".atlassian.net"}
            jira = JIRA(options=jiraOptions, basic_auth=(request.POST['email'], request.POST['apitoken']))
            UserJiraCredentials.objects.update_or_create(token=token, project=request.POST['project'], email=request.POST['email'], jiratoken=request.POST['apitoken'])
            projects = jira.projects()
            if len(projects) == 0:
                JiraIssues.objects.all().delete()
                msg = "There is no projects available"
                context = {'message': msg}
                return render(request, "jiraauthentification.html", context)  
            else:
                JiraIssues.objects.all().delete()
                for prj in projects:
                    for issue in jira.search_issues(jql_str='project='+str(prj)):
                        try:
                            JiraIssues.objects.update_or_create(token=token,
                                                                project=prj,
                                                                issuetype=issue.fields.issuetype,
                                                                issuekey=issue.key,
                                                                issuesummuray=issue.fields.summary,
                                                                issuedescription=issue.fields.description,
                                                                issueassignee=issue.fields.assignee,
                                                                issuereporter=issue.fields.reporter,
                                                                issuepriority=issue.fields.priority,
                                                                issuestatus=issue.fields.status,
                                                                issueresolution=issue.fields.resolution,
                                                                issuecreated=issue.fields.created,
                                                                issueupdated=issue.fields.updated,
                                                                issuedue=issue.fields.duedate)                                     
                        except JIRAError or IntegrityError:
                            pass
                LOI = JiraIssues.objects.all().order_by('issueupdated')
                context = {'list': LOI.reverse(), 'project': request.POST['project']}      
                return render(request, "jiraissues.html", context) 
        except JIRAError:
            return render(request, "oops.html")     
    else:
        try:
            user_activation_token = ActivationTokens.objects.get(token=token) 
        except ActivationTokens.DoesNotExist:
            user_activation_token = None 
        if user_activation_token is not None:
            return render(request, "jiraauthentification.html")     