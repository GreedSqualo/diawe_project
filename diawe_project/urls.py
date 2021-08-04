from diawe import views
from django.contrib import admin
from django.urls import include
from django.conf import settings
# from django.conf.urls.static import static
from django.urls import path
from django.conf.urls.static import static


urlpatterns = [
    path ('',views.user_login,name='login'),   
    path('diawe/',include('diawe.urls')),
    path('admin/', admin.site.urls),
    path('',views.login, name='login'),
    
]
 

 # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
