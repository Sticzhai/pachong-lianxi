import requests
import os,sys
import glob
import threading
#from .models import *



class SaveFile():
    def __init__(self,
                 url = 'http://audio.xmcdn.com/group45/M0B/BF/A7/wKgKjluR79iQHOCIABllDSI8EYg648.m4a',
                 start_num = 0,
                 end_num = None,
                 dir_name = 'content',
                 file_name = 'file'
                 ):
        self.url = url
        self.start_num = start_num
        self.end_num = end_num
        self.dir_name = dir_name
        self.file_name = file_name
        #__save = self.request()

    def header(self):
        headers = {
            'Range': 'bytes={}-{}'.format(self.start_num,self.end_num),
            'Referer': '{}'.format(self.url),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            }
        con_get = requests.get(self.url,headers = headers)
        return con_get

    def request_save(self):
        con = self.header().content
        #os.system('mkdir conten2')
        with open('../{}/{}.con'.format(self.dir_name,self.file_name),'wb') as f:
            f.write(con)

class XunLei(threading.Thread,SaveFile):
    def __init__(self,
                 url = 'http://audio.xmcdn.com/group45/M0B/BF/A7/wKgKjluR79iQHOCIABllDSI8EYg648.m4a',
                 start_num = 0,
                 end_num = None,
                 dir_name = 'content',
                 file_name = 'file'
                 ):
        threading.Thread.__init__(self)
        self.url = url
        self.start_num = start_num
        self.end_num = end_num
        self.dir_name = dir_name
        self.file_name = file_name
        self.info = self.info()

    def info(self):
        #print(self.header().headers)
        num = self.header().headers['Content-Range'].split('/')[-1]
        print(num)
        #print(type(num))
        return num
    def run(self):
        if self.start_num < int(self.info):
            self.request_save()
save_type = ['m4a','mp3','ape','flac']
def run_save(down_url,name = None,arg = 10):
    #print(glob.glob('*'))
    try :
        os.chdir('../content')  # 进入content文件夹
    except:
        os.mkdir('../content')
        os.chdir('../content')
    oldlist_len = len(glob.glob('*'))
    #print(oldlist_len)
    #os.chdir('../../')
    #url = 'http://audio.xmcdn.com/group48/M01/16/CB/wKgKlVtHMKmDkJKAACOcVWmNdlI052.m4a'
    url = down_url  #request.GET['content_url']
    print(int(SaveFile(url,0,9999).header().headers['content-range'].split('/')[1]))
    num = int(SaveFile(url,0,9999).header().headers['content-range'].split('/')[1])//arg
    print(num)
    pool = []
    for i in range(arg):
        print(i + oldlist_len)
        xun = XunLei(url=url,
                     start_num=i * num,
                     end_num=i * num + (num-1),
                     file_name=str(i + oldlist_len))
        pool.append(xun)
    for ii in pool:
        try:
            ii.start()
        except:
            error_id = pool.index(ii)+1
            error_c = sys.exc_info()
            Collect.objects.creat(error_id = error_id,error_type = error_c[0],
                                  error_index = error_c[1])
            print('矮油，出了个小错误！')
            pass
        else:
            print('ok')
            pass
    for iii in pool:
        iii.join()
    # oldlist_len = 0
    #os.chdir('search/content')
    content_list = glob.glob('*')
    print(content_list)
    with open('{}.con'.format(oldlist_len), 'ab') as f:
        for i in range(len(content_list[oldlist_len + 1:])):
            with open('{}.con'.format(oldlist_len+i+1), 'rb') as ff:
                f.write(ff.read())
                print('{}.con'.format(oldlist_len+i+1))
    for i in range(len(content_list[oldlist_len + 1:])):
        os.remove('{}.con'.format(oldlist_len+i+1))
    print('end')
    for save_t in save_type:
        if save_t in down_url and name == None:
            print('ooo')
            with open('{}.mp3'.format(oldlist_len),'wb') as file:
                with open('{}.con'.format(oldlist_len),'rb') as f:
                    file.write(f.read())
            os.remove('{}.con'.format(oldlist_len))
            break
        elif name != None:
            print(name)
            with open('{}'.format(name),'wb') as file:
                with open('{}.con'.format(oldlist_len),'rb') as f:
                    file.write(f.read())
            os.remove('{}.con'.format(oldlist_len))
        else:
            pass
    #os.chdir('../../')

if __name__ == '__main__':
    run_save('http://down.7k7k.com/www/7k7kGame_1.0.4.0.exe')
    '''
    #SaveFile(end = 100000)
    os.chdir('content')  # 进入content文件夹
    oldlist_len = len(glob.glob('*'))
    print(oldlist_len)
    os.chdir('../')
    url = 'http://audio.xmcdn.com/group48/M01/16/CB/wKgKlVtHMKmDkJKAACOcVWmNdlI052.m4a'
    num = int(SaveFile(url=url,).header().headers['Content-Length'])//100000+1
    #print(num)
    pool = []
    for i in range(num):
        print(i)
        xun = XunLei(url=url,
                start_num=i * 100000,
                end_num=i * 100000 + 99999,
                file_name=str(i+oldlist_len))
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
    #oldlist_len = 0
    os.chdir('content')
    content_list = glob.glob('*')
    with open(content_list[oldlist_len],'ab') as f:
        for i in content_list[oldlist_len+1:]:
            with open(i,'rb') as ff:
                f.write(ff.read())
            os.remove(i)
    print('end')


        

'''
'''

url = 'http://audio.xmcdn.com/group45/M0B/BF/A7/wKgKjluR79iQHOCIABllDSI8EYg648.m4a'

headers_a = {
    'Accept': '*/*',
    'Accept-Encoding': 'identity;q=1, *;q=0',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'audio.xmcdn.com',
    'Range': 'bytes=0-',
    'Referer': url,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',

    }

r = requests.get(url,headers = headers_a)


length = r.headers['Content-Length']

length_1 = int(length)//2

headers_b = {
    'Accept': '*/*',
    'Accept-Encoding': 'identity;q=1, *;q=0',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'audio.xmcdn.com',
    'Range': 'bytes=0-{}'.format(length_1),
    'Referer': url,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',

    }
headers_c = {
    'Accept': '*/*',
    'Accept-Encoding': 'identity;q=1, *;q=0',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'audio.xmcdn.com',
    'Range': 'bytes={}-'.format(length_1+1),
    'Referer': url,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',

    }

rr = requests.get(url,headers = headers_b)
with open('b.mp3','wb') as f:
    f.write(rr.content)

rrr = requests.get(url,headers = headers_c)
with open('c.mp3','wb') as f:
    f.write(rrr.content)

'''




















