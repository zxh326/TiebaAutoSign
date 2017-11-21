from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterForm(forms.ModelForm):
    
    # 注册视图

    # class Meta:
    #     model = Register
    #     fields = ('',)
    

class LoginForm(forms.ModelForm):
    # 登陆视图

    # class Meta:
    #     model = Login
    #     fields = ('',)
    pass

class ForgetForm(forms.ModelForm):
    class Meta:
        model = Forget
        fields = ('',)
    

class ResetPasswdForm(forms.ModelForm):
    # 重置密码视图

    # class Meta:
    #     model = MODELNAME
    #     fields = ('',)
    pass


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')
        
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bduss',)