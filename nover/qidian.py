import requests
import json,os
from .spider import *
#from models import *


class QiDian:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    def __init__(self,
                 url='https://www.qidian.com/free',
                 shuming = '<h4><a href=".*?" target="_blank" data-eid=".*?" data-bid="(.*?)">(.*?)</a></h4>.*?'
                         '<a class="name" href="//my.qidian.com/(.*?)" target="_blank" data-eid=".*?">(.*?)</a>',
                 charset='utf-8',
                 json=None,
                 ):
        self.s = requests.Session()
        self.url = url
        self.shuming = shuming
        self.charset = charset
        self.json = json
    def xianmian(self):
        '''
        限免的书的id和链接
        :param 'shuming': [('1011879207', '重生之武神大主播',
         'author/6636557', '忘川三途'),(...)...]
        :return: {'shuming':[book_ID,book_name,author_id,author]}
        '''
        print(self.url)
        print(self.shuming)
        book_all = Spider(self.url,charset='utf-8').info(shuming = self.shuming,)
        #print(Spider(self.url).html)      #不能查看，可以获得
        return book_all
    def xianmian_chapter(self):
        '''
        :return: {'全民进化时代'：{忘川三途':'author/6636557','第一章 重生': 'CJ37WFuiFctwKI0S3HHgow2/aNgDOgvhRGuaGfXRMrUjdw2',...}...}
        '''
        book_all = self.xianmian()
        content = {}
        for i in book_all['shuming']:
            chapter_id = {}
            book_id = i[0]   #1004990373
            book_name = i[1]
            chapter_id[i[3]]=i[2]
            chapter_url = 'https://book.qidian.com/ajax/book/category?_csrfToken=e4UtouFpElcBQA4T3hpNeuDe5WmY7iGJokeiracZ&bookId={}'.format(book_id)
            chapter = Spider(chapter_url,charset='utf-8',json=json).html
            #print(chapter)
            #print(chapter['data']['vs'])
            if len(chapter['data']['vs']) == 3:
                arg1 = 1
                arg2 = 2
            else:
                arg1 = 0
                arg2 = 1
            chapter1 = chapter['data']['vs'][arg1]['cs']
            #print(chapter1)
            for chapter_content in  chapter1:
                chapter1_id = chapter_content['cU']
                chapter1_name = chapter_content['cN']
                chapter_id[chapter1_name] = chapter1_id
            #print(chapter_id)
            chapter2 = chapter['data']['vs'][arg2]['cs']
            #print(chapter2)
            for chapter_content in chapter2:
                chapter2_id = chapter_content['cU']
                chapter2_name = chapter_content['cN']
                chapter_id[chapter2_name] = chapter2_id
            content[book_name] = chapter_id
        print(content)
        return content
    def xianmian_save(self):
        for name,book in self.xianmian_chapter().items():
            for chapter,chapter_id in book.items():
                #print(chapter)
                if '第' in chapter and '章' in chapter:
                    url = 'https://read.qidian.com/chapter/'+chapter_id
                    c_dict = Spider(url,charset='utf-8').info(chapter='<h3 class="j_chapterName">(.*?)</h3>',
                                     content='<div class="read-content j_readContent">(.*?)</div>', )
                    print(c_dict)
                    #print(name)
                    try:
                        os.chdir('{}'.format(name))  # 进入content文件夹
                    except:
                        os.mkdir('{}'.format(name))
                        os.chdir('{}'.format(name))
                        print('ok')
                    #for i in c_dict:
                    with open('{}.txt'.format(c_dict['chapter'][0]),'w') as f:
                        f.write(c_dict['chapter'][0])
                        content = c_dict['content'][0].replace('<p>','\n')
                        f.write(content)
                    print('{}完毕'.format(c_dict['chapter']))
                    os.chdir('../')
                else:
                    pass
class QiDian_free:
    '''
    free/all:
    shuming = '<h4><a href=".*?" target="_blank" data-eid=".*?" data-bid="(.*?)">(.*?)</a></h4>.*?' \
              '<a class="name" href="//my.qidian.com/(.*?)" data-eid=".*?" target="_blank">(.*?)</a>'
    search:
    <h4><a href="//book.qidian.com/info/1010734471" target="_blank" data-eid="qd_S05" data-bid="1010734471"
    data-algrid="0.0.0"><cite class="red-kw">人生</cite>改造计划</a></h4><p class="author">
    <img src="//qidian.gtimg.com/qd/images/ico/user.f22d3.png"><a class="name" data-eid="qd_S06" href="//my.qidian.com/author/401170207" target="_blank">
    笔下银河</a> <em>|</em><a href="//www.qidian.com/dushi" data-eid="qd_S07" target="_blank">都市</a><em>|</em><span>连载中</span>
    '''
    def __init__(self,url='https://www.qidian.com/free/all',
                 shuming = '<h4><a href=".*?" target="_blank" data-eid="qd_S05" data-bid="(.*?)" '
                           'data-algrid="0.0.0">(.*?)</a></h4>.*?<a class="name" data-eid="qd_S06" '
                           'href="//my.qidian.com/(.*?)" target="_blank">(.*?)</a>',):
        self.shuming = shuming
        self.url = url
    def quanmian_book(self,kw):
        '''
        kw: '人生'
        :return:book_all = {'shuming': [('1010734471', '<cite class="red-kw">人生</cite>改造计划', 'author/401170207', '笔下银河'),...]}
        '''
        search_url = 'https://www.qidian.com/search?kw={}&vip=0&page=1'.format(kw)
        #print(self.shuming)
        book_all = QiDian(search_url,self.shuming).xianmian()
        return book_all
    def quanmian_chapter(self,book_id):
        '''
        <li data-rid="3"><a href="//read.qidian.com/chapter/ORlSeSgZ6E-LTMDvzUJZaQ2/-PYP3QgTmoFMs5iq0oQwLQ2"target="_blank" data-eid="qd_G55" data-cid="//read.qidian.com/chapter/ORlSeSgZ6E-LTMDvzUJZaQ2/-PYP3QgmoFMs5iq0oQwLQ2" title="首发时间：2017-11-13 12:18:28 章节字数：3146">第三章 教练，我想要ssr...</a></li>
        :param book_id:  1010734471
        :return:{'chapter': [('ORlSeSgZ6E-LTMDvzUJZaQ2/qsKbX4TnPdTgn4SMoDUcDQ2', '首发时间：2017-11-11 10:48:30 章节字数：3064', '第一章 滴~女朋友卡'),...]}
        '''
        chapter_url = 'https://book.qidian.com/info/{}#Catalog'.format(book_id)
        print(chapter_url)
        chapter = Spider(chapter_url,charset='utf-8').info(
            chapter = '<a href="//read.qidian.com/chapter/(.*?)" '
                      'target="_blank" data-eid="qd_G55" data-cid=".*?" title="(.*?)">(.*?)</a>',)
        chapter['book_id'] = book_id
        return chapter
    def quanmian_content(self,chapter_id):
        '''
        :param chapter_id: 'ORlSeSgZ6E-LTMDvzUJZaQ2/qsKbX4TnPdTgn4SMoDUcDQ2'
        :return: {'chapter': ['第一章 滴~女朋友卡'], 'content': ['\n ...]}
        '''
        url = 'https://read.qidian.com/chapter/'+chapter_id
        c_dict = Spider(url,charset='utf-8').info(chapter='<h3 class="j_chapterName">(.*?)</h3>',
                                  content='<div class="read-content j_readContent">(.*?)</div>', )
        content = c_dict['content'][0].replace('\u3000','\n')
        c_dict['content'] = content
        print(c_dict)
        return c_dict
    def quanmian_page(self,chapter_id):
        '''
        <a id="j_chapterPrev" data-eid="qd_R107"    href="//read.qidian.com/chapter/(.*?)">上一章</a><span>|</span>
        <a href="//book.qidian.com/info/(.*?)#Catalog" target="_blank" data-eid="qd_R108">目录</a><span>|</span>
        <a id="j_chapterNext" href="//read.qidian.com/chapter/(.*?)" data-eid="qd_R109" >下一章</a>
        :param chapter_id:
        :return:
        '''
        url = 'https://read.qidian.com/chapter/'+chapter_id
        page = []
        spage = Spider(url,charset='utf-8').info(spage = '<a id="j_chapterPrev" .*? href="(.*?)">上一章</a><span>|</span><a href="//book.qidian.com/info/.*?#Catalog"',)
        c_id = Spider(url,charset='utf-8').info(c_id = '<a class="act" href=".*?" target="_blank" id="bookImg" data-bid="(.*?)">(.*?)</a>',)
        xpage = Spider(url,charset='utf-8').info(xpage = '<a id="j_chapterNext" href="//read.qidian.com/chapter/(.*?)" data-eid="qd_R109" >下一章</a>',)
        auther = Spider(url,charset='utf-8').info(auther = '<h2><a href="//me.qidian.com/.*?" target="_blank">(.*?)</a>著</h2>',)
        page.append(spage['spage'][0])
        page.append(c_id['c_id'][0])
        page.append(xpage['xpage'][0])
        page.append(auther['auther'][0])
        return page

'''
if __name__ == '__main__':
    #print(QiDian().xianmian())
    #print(QiDian_free('人生').quanmian_chapter(1010734471))
    print(QiDian_free().quanmian_page('ORlSeSgZ6E-LTMDvzUJZaQ2/qsKbX4TnPdTgn4SMoDUcDQ2'))

    x = Spider().info(shuming = '<h4><a href="(.*?)" target="_blank" data-eid=".*?" data-bid=".*?">(.*?)</a></h4>',)
    #print(x)
    for i in x['shuming']:
        shu_url = i[0].split('/')[-1]  #1004990373
        shuming = i[1]
        shu_url = 'https://book.qidian.com/ajax/book/category?_csrfToken=e4UtouFpElcBQA4T3hpNeuDe5WmY7iGJokeiracZ&bookId={}'.format(shu_url)
        print(shu_url)
        chapter = Spider(shu_url,json=json)
    url = 'http://'+xx['n_url'][0][2:]
    #print(url)
    content = Spider(url).html
    #print(Spider(url).info(author = '<h2><a href=".*?">(.*?)</a>著</h2>',
                           chapter = '<h3 class="j_chapterName">(.*?)</h3>',
                           content = '<div class="read-content j_readContent">(.*?)</div>',))
'''
'''
    x = Spider().info(shuming = '<h4><a href="(.*?)" target="_blank" data-eid=".*?" data-bid=".*?">(.*?)</a></h4>',)
    #print(x)
    for i in x['shuming']:
        shu_url = i[0].split('/')[-1]  #1004990373
        shuming = i[1]
        shu_url = 'https://book.qidian.com/ajax/book/category?_csrfToken=e4UtouFpElcBQA4T3hpNeuDe5WmY7iGJokeiracZ&bookId={}'.format(shu_url)
        print(shu_url)
        chapter = Spider(shu_url,json=json)
    url = 'http://'+xx['n_url'][0][2:]
    #print(url)
    content = Spider(url).html
    #print(Spider(url).info(author = '<h2><a href=".*?">(.*?)</a>著</h2>',
                           chapter = '<h3 class="j_chapterName">(.*?)</h3>',
                           content = '<div class="read-content j_readContent">(.*?)</div>',))
'''