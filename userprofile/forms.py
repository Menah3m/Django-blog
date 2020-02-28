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

