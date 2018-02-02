from .forms import *
from .models import *
from .util import get_bname, get_tiebas
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.http.request import QueryDict
from django.contrib import messages
# Create your views here.
UserProfile

def index(request):
    return render(request, 'base1.html',{'title':'demo'})


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


@login_required(login_url='/login')
def update_user_bduss(request):
    if request.method == 'POST':
        info = get_bname(request.POST['bduss'])
        datas = {}
        if info['status'] == 0:
            datas['bduss'] = request.POST['bduss']
            datas['bname'] = info['bname']
            profile_form = ProfileEditForm(instance=request.user.userprofile,
                                           data=datas)
            if profile_form.is_valid():
                profile_form.save()
            else:
                messages.error(request, '信息更新失败')
        else:
            profile_form = ProfileEditForm(instance=request.user.userprofile)
            messages.success(request, 'Bduss 无效')
    else:
        profile_form = ProfileEditForm(instance=request.user.userprofile)

    return render(request,
                  'tieba/edit.html',
                  {'profile_form': profile_form})


def add_user_tieba(request):
    """
        TODO：增量更新 pass
    """
    this_user = UserProfile.objects.get(user_id=request.user.id)

    user_tiebas = TiebaList.objects.filter(user_id=request.user.id)
    user_tiebas = [str(i.fid) for i in user_tiebas]

    # print (user_tiebas)

    user_all_tiebas = get_tiebas(this_user.bduss, this_user.bname)

    user_new_tiebas = []
    to_save_list = []
    for _i in user_all_tiebas:
        if _i[0] not in user_tiebas:
            user_new_tiebas.append(_i)

    for _i in user_new_tiebas:
        one_tieba = TiebaList(fid=_i[0],
                              tiebaname=_i[1],
                              user_id=request.user.id,)
        to_save_list.append(one_tieba)

    TiebaList.objects.bulk_create(to_save_list)
    
    return HttpResponse('Update'+ str(len(user_new_tiebas)))


def flush_all_tieba(request):
    if not request.user.is_admin:
        return HttpResponse(request,'gun')
    else:
        pass

def update_user_tieba(user_id):
    pass


def status_view(request):
    pass


def all_status_view(request):
    pass


def system_setting_view(request):
    pass


def person_setting_view(request):
    pass


def user_manager_view(request):
    pass
