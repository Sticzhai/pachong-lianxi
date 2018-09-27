"""exam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
app_name = 'nover'
urlpatterns = [
    path('',views.choice,name='nover'),
    path('search_book',views.search_book,name = 'search_book'),
    path('search/',views.search,name='search'),
    path('search/<int:book_pk>/<int:book_id>/',views.book,name = 'book'),
    path('search/<int:book_pk>/<int:book_id>/<int:a>/',views.book,name = 'book_save'),
    path('search/<int:book_pk>/<int:book_id>/<int:chapter_id>.html/',views.chapter,
         name = 'chapter'),
    path('q_search/',views.q_search,name = 'q_search'),
    path('q_chapter/<book_id>', views.q_chapter, name='q_chapter'),
    path('q_content/<book_id>/<chapter_id>', views.q_content, name='q_content'),
]























