from django.http import HttpResponse
from django.shortcuts import render
from diawe import models
from django.shortcuts import render, HttpResponse, redirect


def login(request):
    error_msg = ''
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('user', None) #避免提交空，时异常
        username = username.strip() #用户输入末尾有空格是去空格
        password = request.POST.get('pwd')

        obj = models.aUser.objects.filter(name=username, password=password).first()
        if obj:
            # return redirect('/index')
            return redirect('/home/')
            # error_msg = "welcome"
            # return render(request, 'login.html', {'error_msg': error_msg})
        else:
            error_msg = "账号或者密码不对"
            return render(request, 'login.html', {'error_msg': error_msg})
    else:
        return render(request, 'login.html')


def register(request):
    error_msg = ''
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('pwd')
        repeat_password = request.POST.get('repwd')
        email = request.POST.get('email')
        if not username:
            error_msg = "用户名不得为空"
            return render(request, 'register.html', {'error_msg': error_msg})
        if not email:
            error_msg = "email不能为空"
            return render(request, 'register.html', {'error_msg': error_msg})
        if not password:
            error_msg = "密码不能为空"
            return render(request, 'register.html', {'error_msg': error_msg})
        if not repeat_password:
            error_msg = "确认密码不能为空"
            return render(request, 'register.html', {'error_msg': error_msg})
        
        if username and password and repeat_password:
            if password == repeat_password:
                # filter() 函数用于过滤序列，过滤掉不符合条件的元素，返回由符合条件元素组成的新列表
                user_project = models.aUser.objects.filter(name=username).first()
                if user_project:
                    error_msg = "邮箱已存在"
                    return render(request, 'register.html', {'error_msg': error_msg})
 
                else:
                    models.aUser.objects.create(name=username, email=email,password=password).save()
                    # error_msg = "welcome"
                    # return render(request, 'register.html', {'error_msg': error_msg})
                    return redirect('/login/')
            else:
                error_msg = "两次输入的密码不一致"
                return render(request, 'register.html', {'error_msg': error_msg})
                # return HttpResponse('两次输入的密码不一致')

def home(request):
    return render(request, 'home.html')