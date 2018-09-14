
import requests
import re
class Spider:
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',}
    def __init__(self,
                 url = 'https://www.x23us.com/html/28/28373/',
                 charset = 'gbk',
                 json = None,
                 ):
        self.headers = self.headers
        #self.s = requests.Session()
        self.url = url
        self.json = json
        self.charset = charset
        self.html = self.html()
    def html(self):

        res = requests.get(self.url,headers = self.headers)
        res.encoding = self.charset

        if self.json != None:
            return res.json()
        
        return res.text

    def info(self,**regex):
        
        info_dict = {}
        for key,value in regex.items():
            info_dict[key] = re.findall(value,self.html,re.S)

        return info_dict

if __name__ == '__main__':
    pass
    #x = Spider('https://www.ximalaya.com/youshengshu/16897228/',charset = 'utf-8')
    #y = x.info(book_name = '<h1>(.*?)</h1>',book_author = '<h3>(.*?)</h3>',)
    '''
    y = x.info(img_reg = '<dd><a href=".*?" target="_blank"><img src="(.*?)" alt=".*?"></a><br /><a href=".*?" target="_blank">.*?</a></dd>',
               detail_reg = '<dd><a href=".*?" target="_blank"><img src=".*?" alt=".*?"></a><br /><a href="(.*?)" target="_blank">.*?</a></dd>',
               name_reg = '<dd><a href=".*?" target="_blank"><img src=".*?" alt=".*?"></a><br /><a href=".*?" target="_blank">(.*?)</a></dd>',
               )
    '''
    '''
    y = x.info(ty_reg = '<li><p class="ul1">(.*?)《<a class="poptext" href=".*?" target="_blank">.*?</a>》</p><p class="ul2">\
<a href=".*?" target="_blank">.*?</a></p><p>.*?</p>.*?</li>',bknm_reg = '<li><p class="ul1">.*?《<a class="poptext" href=".*?" target="_blank">(.*?)</a>》</p><p class="ul2">\
<a href=".*?" target="_blank">.*?</a></p><p>.*?</p>.*?</li>')
    #print(y)
    '''
    '''
    y = x.info(detail_con='<p style="font-size:16px;color:#333333;line-height:30px;.*?>(.*?)</p>',
               #detail_img='<img data-key=".*?" src="(.*?)" alt="" data-origin="" data-large="" data-large-width=".*?" data-large-height=".*?" data-preview="" data-preview-width=".*?" data-preview-height=".*?" />',
               i = '<img data-key=".*?" src="(.*?)" alt="" data-origin=".*?" data-large=".*?" data-large-width="750" data-large-height=".*?" data-preview=".*?" data-preview-width="140" data-preview-height=".*?" />',
               #ige = '<p style="font-size:16px;color:#333333;line-height:30px;.*?"><img data-key=".*?" src="(.*?)" alt="" data-origin="" data-large="" data-large-width=".*?" data-large-height=".*?" data-preview="" data-preview-width=".*?" data-preview-height=".*?" /></p>',
               )
    #print(x.html)
    print(y)
    '''
