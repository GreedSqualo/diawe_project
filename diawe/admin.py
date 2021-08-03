from django.contrib import admin

from diawe.models import UserProfile
from diawe.models import LogPost

admin.site.register(UserProfile)
admin.site.register(LogPost)