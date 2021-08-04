from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from diawe.forms import  UserForm, UserProfileForm,LogForm
from datetime import datetime
from diawe.models import LogPost, UserProfile
from django.contrib.auth.models import User


@login_required
def index(request):
    # visitor_cookie_handler(request)
    # response = render(request, 'diawe/index.html')
    # return response
    nowuser = request.session.get('nowuser')
    print(nowuser)
    # username = "111"
    return HttpResponse(nowuser)



def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'diawe/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:

                request.session['nowuser'] = username
                login(request, user)
                return redirect(reverse('diawe:article'))
            else:
                
                return HttpResponse("Your Rango account is disabled.")
        else:

            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'diawe/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('diawe:login'))



def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit']= last_visit_cookie
    request.session['visits']= visits



def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def log(request):
    print(request.session.items())
    articles = LogPost.objects.filter(author=request.session['_auth_user_id'])
    # 需要传递给模板（templates）的对象
    context = { 'articles': articles }
    # render函数：载入模板，并返回context对象
    return render(request, 'diawe/article.html', context)

def detail(request,id):
    log = LogPost.objects.get(id=id)
    context = {'article':log}
    return render(request,'diawe/detail.html',context)

def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        log_form = LogForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if log_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = log_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=request.session['_auth_user_id'])
            # 将新文章保存到数据库中
            new_article.save()
            # 完成后返回到文章列表
            return redirect("diawe:article")
            # return render(request, 'diawe/article.html')
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        log_form = LogForm()
        # 赋值上下文
        context = { 'log_form': log_form }
        # 返回模板
        return render(request, 'diawe/create.html', context)