from django.contrib import admin
from django.urls import path
from . import views
app_name = 'xmly'
urlpatterns = [
    path('',views.search,name='xmly'),
    path('search_result/',views.search_result,name = 'search_result'),
    path('album/<int:ab_id>', views.album, name='album'),
    path('zhubo/<int:zhubo_id>', views.zhubo, name='zhubo'),
    path('album/<int:zb_album_id>', views.zb_album, name='zb_album'),

]























