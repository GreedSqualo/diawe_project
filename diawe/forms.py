from django import forms
from django.contrib.auth.models import User
from django.forms import fields
from diawe.models import UserProfile
from diawe.models import LogPost
from diawe.models import Comment
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ( 'picture',)

class LogForm(forms.ModelForm):
    class Meta:
        model = LogPost
        fields = ('title', 'body','picture',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']