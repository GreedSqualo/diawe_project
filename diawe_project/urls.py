from django.contrib import admin
from django.urls import include
from django.conf import settings
# from django.conf.urls.static import static
from django.urls import path
from diawe import models
from diawe import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login, name='login'),
    path('diawe/', include('diawe.urls')),
] # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# from django.conf.urls import url
# from django.contrib import admin
# from diawe import views   # 导入Test应用的views文件

# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     url(r'^login', views.login),
#     url(r'^register', views.register),
# ]
