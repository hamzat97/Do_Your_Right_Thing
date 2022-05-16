from lib2to3.pgen2 import token
from django.db import models

class ActivationTokens(models.Model):
    username = models.CharField(null=False, max_length=50)
    token = models.CharField(null=False, max_length=200)
    class Meta:
        db_table = "ActivationTokens"

class ResetPasswordTokens(models.Model):
    token = models.CharField(null=False, max_length=200)
    class Meta:
        db_table = "ResetPasswordTokens"        

class UserJiraCredentials(models.Model):
    token = models.CharField(null=False, max_length=200)
    project = models.CharField(null=False, max_length=200)
    email = models.EmailField(null=False)
    jiratoken = models.CharField(null=False, max_length=200)
    class Meta:
        db_table = "UserCredentials"       

class JiraIssues(models.Model):
    token = models.CharField(null=False, max_length=200)
    project = models.CharField(null=False, max_length=200)
    issuetype = models.CharField(null=False, max_length=20)
    issuekey = models.CharField(null=False, max_length=20, primary_key=True)
    issuesummuray = models.CharField(null=False, max_length=300)
    issuedescription = models.CharField(null=True, max_length=500)
    issueassignee = models.CharField(null=False, max_length=50)
    issuereporter = models.CharField(null=False, max_length=50) 
    issuepriority = models.CharField(null=False, max_length=20)
    issuestatus = models.CharField(null=False, max_length=20)
    issueresolution = models.CharField(null=True, max_length=20)
    issuecreated = models.DateTimeField(null=False)
    issueupdated = models.DateTimeField(null=False)
    issuedue = models.DateTimeField(null=True)
    class Meta:
        db_table = "JiraIssues" 