from django.contrib import admin

from diawe.models import UserProfile
from diawe.models import LogPost
from diawe.models import Comment

admin.site.register(UserProfile)
admin.site.register(LogPost)
admin.site.register(Comment)