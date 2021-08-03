
from django.urls import path
from diawe import views

app_name = 'diawe'

urlpatterns = [
    path ('',views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('article/', views.log, name='article'),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('create/', views.article_create, name='create'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
]