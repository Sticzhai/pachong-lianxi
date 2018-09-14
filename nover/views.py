from django.shortcuts import render
from django.http import HttpResponseRedirect
from .x23uscom import *
from .spider import *
from .models import *
from django.urls import reverse

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
        return HttpResponseRedirect(reverse('nover:book',args=(arg[0],arg[1])))

    else:
        context = {'info':res_obj.info()}
    
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
    if a == None:
        return render(request,'nover/book.html',context=info_list)
    else:
        try:
            book = BookName.objects.get(bookname = info_list['book_name'],bookauthor = info_list['book_author'])
        except:
            book = BookName.objects.create(bookname=info_list['book_name'][0],
                                           bookauthor=info_list['book_author'][0])
            #print(info_list['book_info'])
            #num = len(info_list['book_info'])//10+1
            x = XiaoShuo(url = url,info_list = info_list,book = book)
            x.start()
            x.join()
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
            '''
                for i in info_list['book_info'][:3]:
                    url = 'https://www.x23us.com/html/{}/{}/{}'.format(book_pk,book_id,i[0])
                    #print(url)
                    chapter = Spider(url).content()
                    #print(chapter)
                    chapter_title = book.bookspider_set.create(bookspider = i[1])
                    chapter_content = chapter_title.content_set.create(content = chapter)
                    #print(info_list['book_name'])
                    with open(r'nover/save-content/书名：'+info_list['book_name'][0]+'-'+'作者：'+info_list['book_author'][0]+'.txt','a') as f :
                        f.write('\n\n')
                        f.write(i[1])
                        f.write('\n\n')
                        f.write(chapter)
                '''
        else:
            chapter_list = book.bookspider_set.only('spider_id')
            c_list = []
            for i in chapter_list:
                c_list.append(i)
            c_list = c_list.sort()
            for chapter in c_list:
                chapter_content = chapter.content_set.all()
                with open(r'nover/save-content/书名：' + info_list['book_name'][0] + '-' + '作者：' +
                          info_list['book_author'][0] + '.txt', 'a') as f:
                    f.write('\n\n')
                    f.write(chapter.bookspider)
                    f.write('\n\n')
                    f.write(chapter_content)
        return render(request, 'nover/save.html', context={})





def chapter(request,book_pk,book_id,chapter_id):
    
    url = 'https://www.x23us.com/html/{}/{}/{}.html'.format(book_pk,book_id,chapter_id)

    chapter_title = '<title>(.*?)</title>'
    chapter_content = '<dd id="contents">(.*)'

    previou_page = '<dd id="footlink"><a href="/html/(.*?)">上一页</a>\
<a href="/html/(.*?)" title=".*?">返回章节列表</a>\
<a href="/html/(.*?)">下一页</a></dd>'
    #next_page = '<a href="(.*?)">下一页</a>'

    x = Spider(url)
    info_list = x.info(chapter_title = chapter_title,
                       chapter_content = chapter_content,
                       previou_page = previou_page,
                       #next_page = next_page,
                       )

    return render(request,'nover/chapter.html',context = info_list)


    
    





























































































    

    

    

    
