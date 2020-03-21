# Name:urls
# Author:Yasu
# Time:2020/3/21
from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    path('post-comment/<int:article_id>/', views.post_comment, name='post_comment'),
]