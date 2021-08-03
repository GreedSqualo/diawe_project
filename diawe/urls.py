from django.conf.urls import url
from django.urls.resolvers import URLPattern
from diawe import views
from django.urls import path

app_name = 'diawe'

urlpatterns = [
    path ('',views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]