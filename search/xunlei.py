import requests
import os
import glob
import threading
from openpyxl import load_workbook


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
        with open('search/{}/{}.con'.format(self.dir_name,self.file_name),'wb') as f:
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
        num = self.header().headers['content-range'].split('/')[1]
        print(num)
        #print(type(num))
        return num

    def run(self):
        if self.start_num < int(self.info):
            self.request_save()

if __name__ == '__main__':
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
            '''
            error_id = pool.index(ii)+1
            error_c = sys.exc_info()
            Collect.objects.creat(error_id = error_id,error_type = error_c[0],
                                  error_index = error_c[1])
            '''
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




















