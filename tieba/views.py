from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from .forms import *
# Create your views here.


def index(request):
    return render(request, 'tieba/index.html')


def register_view(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # profile = UserProfile.objects.create(user=new_user)
            return render(request,
                          'tieba/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = RegisterForm()
    return render(request, 'tieba/register.html', {'form': user_form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # 获取表单用户名和密码
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username, password)
            # 进行用户验证
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                context = {
                    'cardtitle': '登陆成功',
                    'status': 'success',
                }
                return render(request, 'tieba/index.html', context=context)
            else:
                form = LoginForm()
                context = {
                    'cardtitle': '请重新填写信息！',
                    'status': 'error',
                    'form': form,
                }
                return render(request, 'tieba/login.html', context=context)
    else:
        context = {'form': LoginForm(), 'cardtitle': '登录'}

        return render(request, 'tieba/login.html', context=context)


def logout_view(request):
    logout(request)
    return render(request, 'tieba/index.html')


@login_required(login_url='/login')
def edit_view(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.userprofile,
                                       data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '信息更新成功')
        else:
            messages.error(request, '信息更新失败')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.userprofile)
    return render(request,
                  'tieba/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
