# Name:forms
# Author:Yasu
# Time:2020/3/21
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class meta:
        model = Comment
        fields = ['body']