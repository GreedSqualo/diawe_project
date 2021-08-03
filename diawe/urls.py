from django.urls import path
from diawe import views

app_name = 'diawe'

urlpatterns = [
    path('',views.login, name='login'),
    path('register/',views.register, name='register'),
    path('home/',views.home, name='home'),
    path('about/', views.about, name='about'),
]