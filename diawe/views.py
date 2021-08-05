from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from diawe.forms import  UserForm, UserProfileForm,LogForm
from datetime import datetime
from diawe.models import LogPost, UserProfile
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from diawe.models import Comment, Teams
from diawe.forms import CommentForm

@login_required
def index(request):
    visitor_cookie_handler(request)
    response = render(request, 'diawe/index.html')
    return response




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
                return redirect(reverse('diawe:index'))
            else:
                return HttpResponse("Your DiaWe account is disabled.")
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


def log(request, team_id_slug):
    context_dict = {}
    try:
        team = Teams.objects.get(slug=team_id_slug)
        articles = LogPost.objects.filter(team=team)
        # 需要传递给模板（templates）的对象
        context_dict['articles'] =articles
        context_dict['team'] = team
    except Teams.DoesNotExist:
        context_dict['articles'] = None
    # render函数：载入模板，并返回context对象
    return render(request, 'diawe/article.html', context=context_dict)

def detail(request,id):
    #log = LogPost.objects.get(id=id)
    article = LogPost.objects.get(id=id)
    comments = Comment.objects.filter(log=id)
    context = { 'article': article,  'comments': comments }
    return render(request,'diawe/detail.html',context)

def create(request):
    nowuser = request.session.get('nowuser')
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        log_form = LogForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if log_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = log_form.save(commit=False)  
            # 指定当前登录用户为作者
            # new_article.author=request.session.get('nowuser')
            nowuser = request.session.get('nowuser')
            
            new_article.author = User.objects.get(username=nowuser)
            # print(request.session.get('nowuser'))
            # print(User.objects.get(id=1))
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

def about(request):
    return render(request, 'diawe/about.html')

def delete(request, id):
    # 根据 id 获取需要删除的文章
    article = LogPost.objects.get(id=id)
    # 调用.delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect("diawe:article")

def update(request, id):
    # 获取需要修改的具体文章对象
    log = LogPost.objects.get(id=id)
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        log_form = LogForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if log_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            log.title = request.POST['title']
            log.body = request.POST['body']
            log.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("diawe:detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        log_form = LogForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = { 'log': log, 'log_form': log_form }
        # 将响应返回到模板中
        return render(request, 'diawe/update.html', context)



@login_required
def post_comment(request, id):
    log = get_object_or_404(LogPost, id=id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid(): 
            new_comment = comment_form.save(commit=False)
            new_comment.log = LogPost.objects.get(id=id)
            new_comment.author = request.user
            new_comment.save()
            return redirect(log)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接受POST请求。")

def index(request):

    nowuser = request.session.get('nowuser')
    try:
        context_dict = {}
        user = User.objects.get(username=nowuser)
        context_dict['teams'] = user.profile.teams_set.all()
    except user.DoesNotExist or user.profile.DoesNotExist:
        context_dict['teams'] = None
    if request.method == 'POST':
        idTe = request.POST['teamId']
        teamN = request.POST['teamName']
        teamNew = user.profile.teams_set.create(idT=idTe,nameTeam=teamN)
        if teamNew:
            return redirect('/diawe/')
    return render(request, 'diawe/index.html', context=context_dict)