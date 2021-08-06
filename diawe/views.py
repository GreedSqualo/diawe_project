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
    if request.method == "POST":
        try:
            name = request.POST.get('username')
            user = User.objects.get(username=name)
            team.users.add(user.profile)
        except User.DoesNotExist:
            return HttpResponse("User "+name+" does not exist!")
    return render(request, 'diawe/article.html', context=context_dict)

def detail(request,id):
    nowuser = request.session.get('nowuser')
    log = LogPost.objects.get(id=id)
    author = str(log.author)
    users = User.objects.get(username=nowuser)
    picexist = str((log.picture))
    if picexist == "":
        flag = False
        log.picture = "avatar/20210805/b_1v82zMp.png"
    else:
        flag = True
    comments = Comment.objects.filter(log=id)
    context = {'article':log, 'users':users, 'author':author,'flag':flag,'comments':comments}
    return render(request,'diawe/detail.html',context)
    # #log = LogPost.objects.get(id=id)
    # article = LogPost.objects.get(id=id)
    # comments = Comment.objects.filter(log=id)
    # context = { 'article': article,  'comments': comments }
    # return render(request,'diawe/detail.html',context)

def create(request, team_id_slug):
    nowuser = request.session.get('nowuser')
    try: 
        team = Teams.objects.get(slug=team_id_slug)
    except Teams.DoesNotExist:
        team = None
    if team is None :
        return redirect('/diawe/')
  
    if request.method == "POST":
        log_form = LogForm(data=request.POST)

        if log_form.is_valid():
            new_article = log_form.save(commit=False)
            new_article.team = team  
            nowuser = request.session.get('nowuser')
            new_article.author = User.objects.get(username=nowuser)
            
            if 'file' in request.FILES:
                new_article.picture= request.FILES.get('file')

            new_article.save()
          
            return render(request, 'diawe/article.html')
        
        else:
            return HttpResponse("Invalid Form. Please write it again.")
    # 如果用户请求获取数据
    else:
        log_form = LogForm()
        context_dict = { 'log_form': log_form ,'team': team}
        return render(request, 'diawe/create.html', context=context_dict)

def about(request):
    return render(request, 'diawe/about.html')

def delete(request, id):
    article = LogPost.objects.get(id=id)
    article.delete()
    return redirect("diawe:index")

def update(request, id):
   
    log = LogPost.objects.get(id=id)
 
    if request.method == "POST":
  
        log_form = LogForm(data=request.POST)
        if log_form.is_valid():
            log.title = request.POST['title']
            log.body = request.POST['body']
            if 'file' in request.FILES:
                log.picture= request.FILES.get('file')
            log.save()
           
            return redirect("diawe:detail", id=id)
        
        else:
            return HttpResponse("Invalid Form. Please write it again.")

    else:
        log_form = LogForm()
        context = { 'log': log, 'log_form': log_form }
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
    except:
        context_dict['teams'] = None
    if request.method == 'POST':
        idTe = request.POST['teamId']
        teamN = request.POST['teamName']
        teamNew = user.profile.teams_set.create(idT=idTe,nameTeam=teamN)
        if teamNew:
            return redirect('/diawe/')
    return render(request, 'diawe/index.html', context=context_dict)