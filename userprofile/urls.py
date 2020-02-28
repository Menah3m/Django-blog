# Name:urls.py
# Author:Yasu
# Time:2020/2/29

from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]