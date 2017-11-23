from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        t = User.objects.filter(email=email)
        if len(t) != 0:
            raise forms.ValidationError('该邮箱已经注册过了')
        else:
            return email

class LoginForm(forms.Form):
    username = forms.CharField(
        label=u"用户名",
        error_messages={'required': u'请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'class': 'validate',
                # 'placeholder': "用户名",
                'type':'text',
            }
        ),
    )

    password = forms.CharField(
        required=True,
        label=u"密码",
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'class': 'validate',
                # 'placeholder': "密码",
                # 'type': 'password',
            }
        ),
    )


    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"用户名和密码为必填项")
        else:
            cleaned_data = super(LoginForm, self).clean()

class ForgetForm(forms.ModelForm):
    # class Meta:
    #     model = Forget
    #     fields = ('',)
    pass

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