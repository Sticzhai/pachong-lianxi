import requests
import urllib.parse
import re


class X23usCom:
    '''
    搜索关键字，返回关键字列表。
    '''
    def __init__ (self,key_word='大主宰'):
        self.key_word = key_word

    def index(self):
        key_word = self.key_word.encode('gb2312')
        #key_word = urllib.parse.quote(key_word)
        url = 'https://www.x23us.com/modules/article/search.php'
        params = {
            'searchtype':'keywords',
            'searchkey':key_word,
            }
        res = requests.get(url,params=params)
        print(res.url)
        if res.history:
            return {'url':res.url}
        else:
            return res

    def info(self):
        self.html = self.index().text
        book_name = '<td class="odd"><a href=".*?">(.*?)</a></td>'
        book_url = '<td class="even"><a href="https://www.x23us.com/html/(.*?)" target="_blank">.*?</a></td>'
        book_author = '<td class="odd">(\w*?)</td>'
        book_statu = '<td class="even" align="center">(.*?)</td>'

        book_name = re.findall(book_name,self.html)
        #print(len(book_name))
        book_url = re.findall(book_url,self.html)        
        #print(book_url)
        book_author = re.findall(book_author,self.html)
        #print(len(book_author))
        book_statu = re.findall(book_statu,self.html)
        #print(len(book_statu))

        #{'大主宰'
        # ：{author:土豆，url:},...}

        info_dict = {}
        for i in range(len(book_statu)):
            info_dict[book_name[i].replace('<b style="color:red">','').replace('</b>','')] = \
                {'author':book_author[i],
                 'url':book_url[i],
                 'statu':book_statu[i],
                                       }
        print(info_dict)
        return info_dict
    
    

        

        

        

        
if __name__ =='__main__':
    print(X23usCom(key_word='貂蝉').info())
























    
