from django.contrib import admin

from diawe.models import Teams, UserProfile
from diawe.models import LogPost
from diawe.models import Comment

class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('idT',)}

admin.site.register(Teams, TeamAdmin)
admin.site.register(UserProfile)
admin.site.register(LogPost)
admin.site.register(Comment)
