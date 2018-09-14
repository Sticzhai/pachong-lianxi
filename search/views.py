from django.shortcuts import render
from .xunlei import *
from .models import *
import sys,os

# Create your views here.
def search(request):
    context = {}
    return render(request,'search/search.html',context)

def load(request):
    print(glob.glob('*'))
    os.chdir('search/content')  # 进入content文件夹
    oldlist_len = len(glob.glob('*'))
    print(oldlist_len)
    os.chdir('../../')
    #url = 'http://audio.xmcdn.com/group48/M01/16/CB/wKgKlVtHMKmDkJKAACOcVWmNdlI052.m4a'
    url = request.GET['content_url']
    print(int(SaveFile(url,0,99999).header().headers['content-range'].split('/')[1]))
    num = int(SaveFile(url,0,99999).header().headers['content-range'].split('/')[1])//100000+1
    print(num)
    pool = []
    for i in range(num):
        print(i + oldlist_len)
        xun = XunLei(url=url,
                     start_num=i * 100000,
                     end_num=i * 100000 + 99999,
                     file_name=str(i + oldlist_len))
        pool.append(xun)
    for ii in pool:
        try:
            ii.start()
        except requests.exceptions.ConnectionError:
            error_id = pool.index(ii)+1
            error_c = sys.exc_info()
            Collect.objects.creat(error_id = error_id,error_type = error_c[0],
                                  error_index = error_c[1])
            print('矮油，出了个小错误！')
    for iii in pool:
        iii.join()
    # oldlist_len = 0
    os.chdir('search/content')
    content_list = glob.glob('*')
    print(content_list)
    with open(content_list[oldlist_len], 'ab') as f:
        for i in range(len(content_list[oldlist_len + 1:])):
            with open('{}.con'.format(oldlist_len+i+1), 'rb') as ff:
                f.write(ff.read())
    for i in range(len(content_list[oldlist_len + 1:])):
        os.remove('{}.con'.format(oldlist_len+i+1))
    print('end')
    os.chdir('../../')
    context = {}
    return render(request,'search/load.html',context)



