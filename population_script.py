import os
from django.contrib.auth import authenticate

from django.template.defaultfilters import title
os.environ.setdefault('DJANGO_SETTINGS_MODULE','diawe_project.settings')

import django
django.setup()
from diawe.models import Comment, LogPost
from diawe.models import UserProfile,Teams
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect



def populate():

    log_user = [
        {'username':'admin',
        'email':'admin@diawe.com',
        'password':'admin'},
        {'username':'test',
        'email':'test@diawe.com',
        'password':'test'}
    ]

   

    log_teams = [
        {'idT':'111111',
        'nameTeam':'django',
        'user':'admin',
        'slug':'111111'},
        {'idT':'111111',
        'nameTeam':'django',
        'user':'test',
        'slug':'111111'}

    ]

    log_pages = [
        {'title':'django',
        'author':'admin',
        'body':'hello world',
        'slug':'111111'}
    ]
   
    log_comments = [
        {'title':'django',
        'author':'admin',
        'body':'well done'}
    ]


    add_user(log_user)
    add_team(log_teams)
    add_log(log_pages)
    add_comment(log_comments)


def add_user(log_user):
    for i in log_user:
        detail = []
        for j in i:
            detail.append(i[j])
        userinfo = User.objects.filter(username = detail[0])
        if not userinfo.exists():
            c = (User.objects.get_or_create(username=detail[0],email=detail[1],password=detail[2]))[0]
            c.save()
            c.set_password(c.password)
            c.save()
            d = (UserProfile.objects.get_or_create(user = User.objects.get(username=detail[0])))[0]
            d.save()


def add_team(log_teams):
    for i in log_teams:
        detail = []
        for j in i:
            detail.append(i[j])
        userinfo = Teams.objects.filter(idT = detail[0])
        if not userinfo.exists():
            user = User.objects.get(username=detail[2])
            user.profile.teams_set.create(idT=detail[0],nameTeam=detail[1])
        else :
            user = User.objects.get(username=detail[2])
            team = Teams.objects.get(slug=detail[3])
            team.users.add(user.profile)
          

def add_log(log_pages):
    for i in log_pages:
        detail = []
        for j in i:
            detail.append(i[j])
        team = Teams.objects.get(slug=detail[3])
        c = LogPost.objects.get_or_create(author=User.objects.get(username=detail[1]),title=detail[0],body=detail[2],team =team)[0]
        c.save()
   #title author body     

def add_comment(log_comments):
    for i in log_comments:
        detail = []
        for j in i:
            detail.append(i[j])
        id = (LogPost.objects.get(title=detail[0])).id
        log = LogPost.objects.get(id=id)
        c = (Comment.objects.get_or_create(log=log,author=User.objects.get(username=detail[1]),body=detail[2]))[0]

        
    
       
if __name__ =='__main__':
    populate()