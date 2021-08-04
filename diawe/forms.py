from django import forms
from django.contrib.auth.models import User
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
        # 指明数据模型来源
        model = LogPost
        # 定义表单包含的字段
        fields = ('title', 'body','picture',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)