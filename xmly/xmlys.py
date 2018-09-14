'''
专辑页面：
https://www.ximalaya.com/ertong/4436043/

源代码：
{"index":293,"trackId":120323263,
"isPaid":false,"tag":0,
"title":"【安全系列】台风来了",
"playCount":5250,"showLikeBtn":true,
"isLike":false,"showShareBtn":true,
"showCommentBtn":true,"showForwardBtn":true,
"createDateFormat":"1天前",
"url":"/ertong/4436043/120323263"}

隐藏真实音乐地址的链接：
https://www.ximalaya.com/revision/play/tracks?trackIds=119781951

'''

import requests
import re
import threading
import glob
import os
import json
from spider import *


class Xm:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36', }

    def __init__(self,
                 key_word,
                 page_num=1,
                 total_page=4,
                 charset='utf-8',
                 main_url='https://www.ximalaya.com',
                 album_url='<a title=".*?" class="xm-album-title ellipsis-2" href="(.*?)">.*?</a><p title=".*?" class="ellipsis createBy">by：<a href=".*?">.*?</a></p></div></span>',
                 album_name='<a title=".*?" class="xm-album-title ellipsis-2" href=".*?">(.*?)</a><p title=".*?" class="ellipsis createBy">by：<a href=".*?">.*?</a></p></div></span>',
                 zb_url='<a title=".*?" class="xm-album-title ellipsis-2" href=".*?">.*?</a><p title=".*?" class="ellipsis createBy">by：<a href="(.*?)">.*?</a></p></div></span>',
                 zb_name='<a title=".*?" class="xm-album-title ellipsis-2" href=".*?">.*?</a><p title=".*?" class="ellipsis createBy">by：<a href=".*?">(.*?)</a></p></div></span>',
                 img_url='<img style="width:100%;height:100%" src="(.*?)"/>'
                 ):
        self.search_url = 'https://www.ximalaya.com/search/{}/sc/p{}'.format(key_word, page_num)
        self.s = requests.Session()
        self.s.headers.update(self.headers)
        self.charset = charset
        self.total_page = total_page
        # self.zb_url = 'https://www.ximalaya.com/{}'.ormat()
        self.main_url = main_url

        self.album_url = album_url
        self.album_name = album_name
        self.zb_url = zb_url
        self.zb_name = zb_name
        self.img_url = img_url

        self.album_dict = self.get_album()
        self.get_info = self.get_info()

    def get_album(self):
        '''
        得到搜索结果，并求出内容，返回一个字典
        '''
        res_h5 = self.s.get(self.search_url)
        # print(res_h5.text)
        res_charset = self.charset
        res_info = res_h5.text

        album_url_list = re.findall(self.album_url, res_info)
        album_name_list = re.findall(self.album_name, res_info)
        print(album_name_list)
        # print(len(album_name_list))
        zb_url_list = re.findall(self.zb_url, res_info)
        zb_name_list = re.findall(self.zb_name, res_info)
        img_url_list = re.findall(self.img_url, res_info)

        ab_dict = {}
        for x in range(len(album_name_list)):
            ab_dict[album_name_list[x]] = {'album_url': album_url_list[x],
                                           'img_url': img_url_list[x],
                                           'zb_name': zb_name_list[x],
                                           'zb_url': zb_url_list[x],
                                           }

        return ab_dict

    def get_info(self):
        album_dict = self.album_dict
        for ab_name, ab_info in album_dict.items():
            ab_url = self.main_url + ab_info['album_url']
            print(ab_url)
            ab_h5 = Spider(url=ab_url, charset='utf-8')
            ab_info.update(
                ab_h5.info(detail_con='<p style="font-size:16px;color:#333333;line-height:30px;.*?>(.*?)</p>',
                           detail_img='<img data-key=".*?" src="(.*?)" alt="" data-origin=".*?" data-large=".*?" data-large-width="750" data-large-height=".*?" data-preview=".*?" data-preview-width="140" data-preview-height=".*?" />',
                           ))

        return album_dict

    def album_detail(self):
        album_dict = self.get_info
        detail_dict = {}
        for ab_name, ab_info in album_dict.items():
            ab_url = self.main_url + ab_info['album_url']
            split_info = ab_url.split('/')[-3:]
            pk = split_info[1]
            info_url = 'https://www.ximalaya.com/revision/play/album?\
albumId={}&pageNum={}&sort=-1&pageSize=30'.format(pk, 1)
            print(info_url)
            detail_dict[ab_name] = {}
            detail_info_list = self.s.get(info_url).json()['data']['tracksAudioPlay']
            print(detail_info_list)
            for i in detail_info_list:
                detail_src = i['src']
                detail_name = i['trackName']
                detail_url = i['trackUrl']
                detail_dict[ab_name].update({detail_name: {'detail_src': detail_src,
                                                           # 'detail_name':detail_name,
                                                           'detail_url': detail_url, }})
        print(detail_dict)

    def save_m4a(self):
        audio_list = self.info['data']['tracksAudioPlay'][:5]
        for a in audio_list:
            src = a['src']
            name = a['trackName']
            print('正在下载：{}'.format(name))

            with open('{}.mp3'.format(name), 'wb') as f:
                f.write(self.s.get(src).content)


if __name__ == '__main__':
    x = Xm('如懿传')
    print(x.album_detail())

'''
class Ximalaya(threading.Thread):

    headers = {#'Accept':'*/*',
               #'Accept-Encoding':'gzip, deflate, br',
               #'Accept-Language':'zh-CN,zh;q=0.9',
               #'Connection':'keep-alive',
               #'Content-Type':'application/json',
               #'Host':'xdcs-collector.ximalaya.com',
               #'Origin':'https://www.ximalaya.com',
               #'Referer':'https://www.ximalaya.com/',
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
               }

    def __init__(self,
                 url = 'https://www.ximalaya.com/ertong/260744/p1/',
                 charset = 'utf-8'):
        threading.Thread.__init__(self)
        self.s = requests.Session()
        self.s.headers.update(self.headers)
        self.url = url
        self.charset = charset

        self.info = self.get_info()['data']['tracksAudioPlay']
        self.thread_pool = self.thread_pool

    def get_info(self):
        split_info = self.url.split('/')[-3:]
        pk = split_info[0]
        page_num = split_info[1].replace('p','')

        info_url = 'https://www.ximalaya.com/revision/play/album?\
albumId={}&pageNum={}&sort=-1&pageSize=30'.format(pk,page_num)
        print(info_url)
        return self.s.get(info_url).json()

    def thread_pool(self):

        if glob.glob('thread.json'):
            pass
        else:
            thread_pool = self.info
            thread_pool_iter = iter(thread_pool)
            with open('thread.json','w') as f:
                f.write(json.dumps(thread_pool))
            with open('now.json','w') as ff:
                ff.write(json.dumps('0'))

        return self.get_info['data']['tracksAudioPlay']

    def save_m4a(self):
        audio_list = self.info['data']['tracksAudioPlay'][:5]
        for a in audio_list:
            src = a['src']
            name = a['trackName']
            print('正在下载：{}'.format(name))

            with open('{}.mp3'.format(name),'wb') as f:
                f.write(self.s.get(src).content)
    def run(self):
        if glob.glob('now.json'):
            with open('now.json') as f:
                i = json.loads(f)

            #i = next(self.thread_pool)
            src = i['src']
            name = i['trackName']
            print('正在下载：{}'.format(name))
            with open('{}.mp3'.format(name),'wb') as f:
                f.write(self.s.get(src).content)

if __name__ == '__main__':

    x = Ximalaya()
    y = x.save_m4a()
    #print(y)
    import threading
    import time

    exitFlag = 0

    class myThread(threading.Thread):

        def __init__(self,threadID,name,counter):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.counter = counter

        def run(self):
            print('开始线程：'+self.name)
            print_time(self.name,self.counter,5)
            print('退出线程：'+self.name)

    def print_time(threadName,delay,counter):
        while counter:
            if exitFlag:
                threadName.exit()
            time.sleep(delay)
            print('%s:%s'%(threadName,time.ctime(time.time())))
            counter -= 1

    #创建新线程
    thread1 = myThread(1,'Thread-1',1)
    thread2 = myThread(2,'Thread-2',2)

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    print('退出主线程')
'''















