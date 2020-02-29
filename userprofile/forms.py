# Name:forms.py
# Author:Yasu
# Time:2020/2/28

# 引入表单类
from django import forms
# 引入User模型
from django.contrib.auth.models import User


# 登录表单，继承了forms.Form类
# forms.Form适用于不和数据库进行交互的功能，比如用户登录
# forms.ModelForm适用于需要直接与数据库交互的功能，比如增删改
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

# 注册用户表单
class UserRegisterForm(forms.ModelForm):
    # 复写User密码
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username','email')

    # 对两次输入的密码一致性进行检查
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致，请重试。")

