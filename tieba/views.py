from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .util import get_tieba_list
from .models import *
from .forms import *
from .do import doo
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


def update_user_bduss(request):
    if request.method == 'POST':
        profile_form = ProfileEditForm(instance=request.user.userprofile,
                                       data=request.POST)
        if profile_form.is_valid():
            profile_form.save()
            if add_user_tieba(request.user.id):
                messages.success(request, 'Success')
            else:
                messages.success(request, 'Bduss 无效')
        else:
            messages.error(request, '信息更新失败')
    else:
        profile_form = ProfileEditForm(instance=request.user.userprofile)
    return render(request,
                  'tieba/edit.html',
                  {'profile_form': profile_form})


def add_user_tieba(user_id):
    this_user = UserProfile.objects.get(user_id=user_id)
    print(this_user.bduss)
    user_tiebas = get_tieba_list(this_user.bduss)
    if user_tiebas['uname'] == 'null' or user_tiebas['uname'] == '':
        return False
    else:
        this_user.user.first_name = user_tiebas['uname']
        this_user.user.save()
        # 第一次获取
        to_save_list = []

        for _i in user_tiebas['tiebas']:
            one_tieba = TiebaList(
                fid=_i[0], tiebaname=_i[1], user_id=user_id)
            to_save_list.append(one_tieba)

        TiebaList.objects.bulk_create(to_save_list)

        return True


def update_user_tieba(user_id):
    pass


def test(request):
    doo()
    return HttpResponse('1')
