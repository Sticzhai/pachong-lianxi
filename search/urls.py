from django.contrib import admin
from django.urls import path
from . import views
app_name = 'search'
urlpatterns = [
    path('',views.search,name='search'),
    path('下载文件/',views.load,name = 'load'),
]























