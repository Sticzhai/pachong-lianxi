from django.shortcuts import render
from .xunlei import *
from .models import *
import sys,os

# Create your views here.
def search(request):
    context = {}
    return render(request,'search/search.html',context)

def load(request):
    url = request.GET['content_url']
    name = request.GET['name_g']
    print(name)
    run_save(url,name)
    context = {}
    return render(request,'search/load.html',context)



