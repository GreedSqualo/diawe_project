import os
from django.contrib.auth import authenticate

from django.template.defaultfilters import title
os.environ.setdefault('DJANGO_SETTINGS_MODULE','diawe_project.settings')

import django
django.setup()
from diawe.models import LogPost
from diawe.models import User




def populate():
    log_pages = [
        {'title':'django',
        'author':'admin',
        'body':'hello world'}
    ]

    log_user = [
        {'username':'admin',
        'email':'admin@diawe.com',
        'password':'admin'}
    ]

    add_user(log_user)
    add_log(log_pages)




def add_user(log_user):
    for i in log_user:
        detail = []
        for j in i:
            detail.append(i[j])
        if authenticate(username=detail[0]) == False:
            c = (User.objects.get_or_create(username=detail[0],email=detail[1],password=detail[2]))[0]
            c.save()
            c.set_password(c.password)
            c.save()

def add_log(log_pages):
    for i in log_pages:
        detail = []
        for j in i:
            detail.append(i[j])
        c = LogPost.objects.get_or_create(author=User.objects.get(username=detail[1]),title=detail[0],body=detail[2])[0]
        c.save()
       
if __name__ =='__main__':
    populate()