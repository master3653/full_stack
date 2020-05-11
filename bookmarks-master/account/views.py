from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm,UserRegistrationForm,UserEditForm,ProfileEditForm
from .models import Profile,Contact
from django.db import transaction
from django.contrib import messages
from django.shortcuts import  render,HttpResponseRedirect # reverse url逆向解析

from django.contrib.auth.models import User
import json
import time
from django.conf import settings
from oauth.models import OAuthQQ
from .oauth_client import OAuthQQ
from django.core.urlresolvers import reverse
import hashlib
from oauth import models as models1

from django.shortcuts import get_object_or_404

from common.decorators import ajax_required
from django.views.decorators.http import require_POST

from actions.utils import create_action
from actions.models import Action
from .models import Profile
# Create your views here.


# Create your views here.

def user_login(request):#用户登录
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('Authenticated successfuly')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request,'account/login.html',{'form':form})

#装饰器检验用户是否通过认证，如果通过，则执行视图，如果没有通过则返回登录页面
@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',flat=True)
    if following_ids:   # select_related取回一对多的关联对象，prefetch_related提高执行效率
        actions = actions.filter(user_id__in=following_ids).select_related('user','user__profile').prefetch_related('target')
    actions = actions[:10]

    return render(request,'account/dashboard.html',{'section':'dashboard','actions':actions})#sction跟踪当前页面

def register(request):
    if request.method=='POST':
        user_form=UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user=user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])

            new_user.save()
            profile = Profile.objects.create(user=new_user)  # 创建Profile对象
            create_action(new_user,'注册了')   #监测相似操作
            return render(request,'account/register_done.html',{'new_user':new_user})
    else:
        user_form=UserRegistrationForm()
    return render(request,'account/register.html',{'user_form':user_form})

@login_required
def edit(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=profile,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '用户编辑成功')
        else:
            messages.error(request, '用户编辑失败')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=profile)
    return render(request, 'account/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form})
@login_required
def user_list(request):     #用户列表
    users=User.objects.filter(is_active=True)
    return render(request,'account/user/list.html',{'sections':'people','users':users})


@login_required
def user_detail(request,username):  #用户详情
    user=get_object_or_404(User,username=username,is_active=True)
    return render(request,'account/user/detail.html',{'sections':'people','user':user})


@ajax_required
@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            print("1")
            if action == 'follow':
                print("2")
                Contact.objects.get_or_create(user_from=request.user,user_to=user)
                create_action(request.user, '关注了', user)
                print("3")

                print('follow')
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
                print('fo')
            return JsonResponse({'status':'OK'})
        except User.DoesNotExist:
            return JsonResponse({'status':'KO'})
    return JsonResponse({'status':'KO'})


def hash_sha256(password, username):  # sha256加密
    sha256 = hashlib.sha256()
    sha256.update((password + username).encode('utf-8'))
    sha256_password = sha256.hexdigest()
    return sha256_password



def qq_login(request):
    oauth_qq = OAuthQQ(settings.QQ_KEY, settings.QQ_SECRET, settings.QQ_RECALL_URL)

    #获取 得到Authorization Code的地址
    url = oauth_qq.get_auth_url()
    #重定向到授权页面
    return HttpResponseRedirect(url)

def qq_check(request):  # 第三方QQ登录，回调函数
    """登录之后，会跳转到这里。需要判断code和state"""
    request_code = request.GET.get('code')
    print("123")
    oauth_qq = OAuthQQ(settings.QQ_KEY, settings.QQ_SECRET, settings.QQ_RECALL_URL)
    print("1")
    # 获取access_token
    access_token = oauth_qq.get_access_token(request_code)
    if access_token:
        print(access_token)
    else:
        print("出错了")
    print("2")
    time.sleep(0.05)  # 稍微休息一下，避免发送urlopen的10060错误
    open_id = oauth_qq.get_open_id()
    print("3")
    #print (open_id)

    # 检查open_id是否存在
    qq_open_id = models1.OAuthQQ.objects.filter(qq_openid=str(open_id))
    #print (qq_open_id)
    print("4")
    if qq_open_id:
        # 存在则获取对应的用户，并登录
        user = qq_open_id[0].user.username
        #print (user)
        request.session['username'] = user
        return HttpResponseRedirect('/account/')
    else:
        # 不存在，则跳转到绑定用户页面
        infos = oauth_qq.get_qq_info()  # 获取用户信息
        print(infos)
        url = '%s?open_id=%s&nickname=%s' % (reverse('bind_account'), open_id, infos['nickname'])
        return HttpResponseRedirect(url)

def bind_account(request):  # 绑定账户
    open_id = request.GET.get('open_id')
    nickname = request.GET.get('nickname')
    if request.method == 'POST' and request.POST:
        data = request.POST # 接收到前台form表单传过来的注册账户信息
        user = User()
        username = data['username']
        password = data['password'].split(',')[0]
        user.username = username
        password = hash_sha256(password, username)
        user.password = password
        user.nickname = data['nickname']
        user.departments_id = 1
        user.save()
        oauthqq = models1.OAuthQQ()
        oauthqq.qq_openid = open_id
        oauthqq.user_id = User.objects.get(username=username).id
        oauthqq.save()
        response = HttpResponseRedirect("/account/")
        request.session['username'] = username  # 设置session
        return response  # 返回首页
    return render(request, 'qq-bind-account.html', locals())



