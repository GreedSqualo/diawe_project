
from django.urls import path
from diawe import views

app_name = 'diawe'

urlpatterns = [
    path ('',views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('article/<slug:team_id_slug>/', views.log, name='article'),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('update/<int:id>/', views.update, name='update'),
    path('post-comment/<int:id>/', views.post_comment, name='post_comment'),
]