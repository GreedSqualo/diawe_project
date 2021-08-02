# from django.contrib import admin
# from django.urls import path
# from diawe import models

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
from django.conf.urls import url
from django.contrib import admin
from diawe import views   # 导入Test应用的views文件

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login', views.login),
    url(r'^register', views.register),
]
