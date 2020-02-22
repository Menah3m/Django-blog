# Name:urls.py
# Author:Yasu
# Time:2020/2/16
from . import views
from django.urls import path

app_name = 'article'

urlpatterns = [
    path('article-list/', views.article_list, name='article_list'),
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),
]
