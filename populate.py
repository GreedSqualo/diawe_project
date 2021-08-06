import os
from django.contrib.auth import authenticate

from django.template.defaultfilters import title
os.environ.setdefault('DJANGO_SETTINGS_MODULE','diawe_project.settings')

import django
django.setup()
from diawe.models import LogPost
from diawe.models import User
from diawe.models import Teams
from diawe.models import Comment
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','tango_with_django_project.settings')




def populate():

    log_user = [
        {'username':'admin',
        'email':'admin@diawe.com',
        'password':'admin'}
    ]

    add_user(log_user)





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


       
if __name__ =='__main__':
    populate()