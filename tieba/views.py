from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from .forms import *
# Create your views here.

def index(request):
    return render(request,'base.html')

def edit(request):
    if request.method == 'POST':
            user_form = UserEditForm(instance=request.user,
                                    data=request.POST)
            profile_form = ProfileEditForm(instance=request.user.userprofile,
                                            data=request.POST)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request,'信息更新成功')
            else:
                messages.error(request,'信息更新失败')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.userprofile)
    return render(request,
                'tieba/edit.html',
                {'user_form': user_form,
                'profile_form': profile_form})
