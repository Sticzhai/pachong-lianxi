from django.shortcuts import render
from django.http import HttpResponseRedirect
from .x23uscom import *
from django.urls import reverse
from .qidian import *

# Create your views here.
def choice(request):
    context = {}
    return render(request, 'nover/choice.html', context)

def search_book(request):
    context = {}
    return render(request,'nover/search_book.html',context)
    
def search(request):
    key_word = request.GET['key_word']
    res_obj = X23usCom(key_word)
    test = res_obj.index()
    if isinstance(test,(dict,)):
        url = test['url']
        chapter = Spider(url)
        info = chapter.info(chapter_url = '<a class="read" href="https://www.x23us.com/html/(.*?)" title=".*?">章节列表</a>')
        print(info)
        arg = info['chapter_url'][0].split('/')
        print(arg)
        return HttpResponseRedirect(reverse('nover:book',args=(arg[0],arg[1])))
    else:
        context = {'info':res_obj.info()}
        for i in res_obj.info().keys():
            try:
                Poll.objects.create(name=i,poll_num = 0)
            except:
                pass
        return render(request,'nover/search.html',context)

def book(request,book_pk,book_id,a = None):
    url = 'https://www.x23us.com/html/{}/{}/'.format(book_pk,book_id)
    book_name = '<meta name="og:novel:book_name" content="(.*?)"/>'
    book_author = '<meta name="og:novel:author" content="(.*?)"/>'
    book_info = '<td class="L"><a href="(.*?)">(.*?)</a></td>'
    xx = Spider(url)
    info_list = xx.info(book_name = book_name,book_author = book_author,book_info = book_info,)
    info_list['book_pk']=book_pk
    info_list['book_id']=book_id
    try:
        votes = Poll.objects.get(name = info_list['book_name'][0])
    except:
        pass
    else:
        votes.poll_num += 1
        votes.save()
        if votes.poll_num > 10:
            try:
                BookName.objects.get(bookname=info_list['book_name'][0],
                                     bookauthor=info_list['book_author'][0])
            except:
                book = BookName.objects.create(bookname=info_list['book_name'][0],
                                               bookauthor=info_list['book_author'][0])
                # print(info_list['book_info'])
                # num = len(info_list['book_info'])//10+1
                x = XiaoShuo(url=url, info_list=info_list, book=book)
                x.start()
                x.join()
                print('完毕！')
    if a == None:
        return render(request,'nover/book.html',context=info_list)
    else:
        try:
            book = BookName.objects.get(bookname = info_list['book_name'][0],
                                        bookauthor = info_list['book_author'][0])
        except:
            book = BookName.objects.create(bookname=info_list['book_name'][0],
                                           bookauthor=info_list['book_author'][0])
            #print(info_list['book_info'])
            num = len(info_list['book_info'])//10+1
            pool = []
            for n in range(num):
                pool.append(XiaoShuo(url = url,info_list = info_list,book = book))
            for x in pool:
                x.start()
                print('\n')
            for i in pool:
                i.join()
            print('完毕！')
            chapter_list = book.bookspider_set.all()
            #print(chapter_list)
            for chapter in chapter_list:
                chapter_content = chapter.content_set.all()
                with open(r'nover/save-content/书名：' + info_list['book_name'][0] + '-' + '作者：' +
                info_list['book_author'][0] + '.txt', 'a') as f:
                    f.write('\n\n')
                    f.write(chapter.bookspider)
                    f.write('\n\n')
                    f.write(chapter_content)
            return render(request, 'nover/save.html', context={})
        else:
            chapter_list = book.bookspider_set.order_by('spider_id')
            #print(chapter_list)
            for chapter in chapter_list:
                #print(chapter)
                chapter_content = Content.objects.get(bookspider = chapter)
                print(chapter_content.content)
                with open(r'nover/save-content/书名：' + info_list['book_name'][0] + '-' + '作者：' +
                          info_list['book_author'][0] + '.txt', 'a') as f:
                    f.write('\n\n')
                    f.write(chapter.bookspider)
                    f.write('\n\n')
                    f.write(chapter_content.content)
            return render(request, 'nover/save.html', context={})

def chapter(request,book_pk,book_id,chapter_id):
    url = 'https://www.x23us.com/html/{}/{}/{}.html'.format(book_pk,book_id,chapter_id)
    chapter_title = '<title>(.*?)</title>'
    chapter_content = '<dd id="contents">(.*)'
    previou_page = '<dd id="footlink"><a href="/html/(.*?)">上一页</a>' \
                   '<a href="/html/(.*?)" title=".*?">返回章节列表</a>' \
                   '<a href="/html/(.*?)">下一页</a></dd>'
    #next_page = '<a href="(.*?)">下一页</a>'
    x = Spider(url)
    info_list = x.info(chapter_title = chapter_title,
                       chapter_content = chapter_content,
                       previou_page = previou_page,
                       )

    return render(request,'nover/chapter.html',context = info_list)

def q_search(request):
    book_key = request.GET['book_key']
    book_list = QiDian_free().quanmian_book(book_key)['shuming']
    context = {'book':book_list}
    return render(request, 'nover/q_search.html', context)

def q_chapter(request,book_id):
    print(book_id)
    chapter_dict = QiDian_free().quanmian_chapter(book_id)
    book_page = QiDian_free().quanmian_page(chapter_dict['chapter'][0][0])
    context = {'book_name':book_page[1][1],'book_author':book_page[3],'chapter':chapter_dict}
    return render(request, 'nover/q_chapter.html', context)

def q_content(request,book_id,chapter_id):
    print(book_id)
    print(chapter_id)
    chapter_dict = QiDian_free().quanmian_chapter(book_id)['chapter'][int(chapter_id)-1]
    content = QiDian_free().quanmian_content(chapter_dict[0])
    context = content
    context['spage'] = int(chapter_id)-1
    context['xpage'] = int(chapter_id)+1
    context['book_id'] = book_id
    return render(request, 'nover/q_content.html', context)
'''
    except:
        return HttpResponseRedirect(reverse('nover:q_chapter',args=(book_id,)))
'''


























































































    

    

    

    
