from django.urls import path
from . import views

urlpatterns = [  
  path('', views.Home),
  path('signin', views.SignIn),
  path('signup', views.SignUp),
  path('resetpassword', views.ForgotPassword),
  path('activateaccount/<uid>/<token>', views.ActivateAccount),
  path('resetpassword/<uid>/<token>', views.ResetPassword),
  path('signin/jiradirectaccess/<username>', views.JiraDirectAccess),
  path('signin/jiraaccess/<token>', views.JiraAccess)
]