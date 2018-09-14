import requests
import threading
import glob
import os
import sys
import json
import re
from .models import *

class Spider:
    
    def __init__(self,
                 url='https://www.x23us.com/html/70/70640/',
                 charset='gbk',
                 json = None,

                 ):

        self.url = url
        self.json = json
        self.charset = charset
        self.html = self.html()

    def html(self):
        '''
        返回网页源代码
        '''
        res = requests.get(self.url)
        res.encoding = self.charset
        if self.json != None:
            return res.json()
        return res.text

    def info(self,**regex):
        '''
        在同一网页源代码中，返回所有想得到的正则内容
        '''
        info_dict = {}
        for key,value in regex.items():
            info_dict[key]=re.findall(value,self.html)
        return info_dict

    def content(self,kongge = '&nbsp;',br ='<br />',
                 regular = '<dd id="contents">(.*?)</dd>'):
        capter_html = requests.get(self.url)
        capter_html.encoding = self.charset
        capter_html = capter_html.text
        #print(capter_html)
        content = re.findall(regular,capter_html,re.S)
        content = content[0].replace(kongge, '').replace(br, '\n')
        #print(content)
        return content      #章节内容
        
class XiaoShuo(threading.Thread):
    '''
    已知：字典info_list，其中有：{'book_name': ['吞噬进化'],
    'book_author': ['育'],
    'book_info': [('30951301', '001 活着'), ('30951302', '002 临别'),
    ('30951303', '003 晶核')]}
    chapter_url = info_list['book_info'][arg][0]
    url = 'https://www.x23us.com/html/70/70640/'
    '''
    def __init__(self,url,info_list,book):
        threading.Thread.__init__(self)
        self.url = url
        self.info_list = info_list
        self.thread_pool()
        self.book = book
    def thread_pool(self):
        if glob.glob(r'nover/save-content/jishu.json'):
            #print('存在')
            pass
        else:
            with open(r'nover/save-content/jishu.json','w') as f:
                f.write(json.dumps('0'))
                print('0')
    def run(self):
        for xx in range(10): #len(self.info_list['book_info'])):
            if glob.glob(r'nover/save-content/jishu.json'):
                with open(r'nover/save-content/jishu.json') as ff:
                    site = int(json.load(ff))
                if site == 20 : #len(self.info_list['book_info']):
                    print('本小说下载完毕！')
                    with open('nover/save-content/jishu.json','w') as f:
                        f.write(json.dumps('0'))
                else:
                    with open ('nover/save-content/jishu.json','w') as f:
                        f.write(json.dumps(str(site+1)))
                        #print(site+1)
                    arg = self.info_list['book_info'][site][0]
                    url = self.url+arg
                    print(url)
                    chaptercontent = Spider(url).content()
                    #写入数据库
                    chapter_title = self.book.bookspider_set.create(spider_id = site,
                                                    bookspider = self.info_list['book_info'][site][1])
                    chapter_title.content_set.create(content = chaptercontent)
                    print('正在下载第{}章'.format(site))

            
        
    
if __name__ == '__main__':
    x = Spider('https://www.x23us.com/html/70/70640/')
    info = x.info(book_name = '<meta name="og:novel:book_name" content="(.*?)"/>',
    book_author = '<meta name="og:novel:author" content="(.*?)"/>',
    book_info = '<td class="L"><a href="(.*?).html">(.*?)</a></td>',)
    '''
    info：返回的内容
    {'book_name': ['吞噬进化'],
    'book_author': ['育'],
    'book_info': [('30951301', '001 活着'), ('30951302', '002 临别'),
    ('30951303', '003 晶核')]}
    '''
    #xinfo = x.content()
    #print(info)
    info_list = info
    thread_lock1 = threading.Lock()
    thread_lock2 = threading.Lock()
    url = 'https://www.x23us.com/html/70/70640/'
    pool = []
    num = len(info_list['book_info'])
    for i in range(num):
        pool.append(XiaoShuo(url,info_list))
    for x in pool:
        x.start()
        print('\n')
    for i in pool:
        i.join()
    print('完毕！')
    





















    
