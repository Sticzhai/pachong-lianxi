'''
主页面：
'https://www.ximalaya.com/'
搜索结果页面（json）：
'https://www.ximalaya.com/revision/search?core=album&kw={}&
spellchecker=true&rows=20'.format(搜索名字)
'https://www.ximalaya.com/revision/search?core=album&kw={}&page={}&
spellchecker=true&rows=20'.format(搜索名字，页数)
搜索结果个数：
['data']['result']['response']['numFound']
专辑名：
['data']['result']['response']['docs'][arg]['title']
第arg个专辑url和图片url：
['data']['result']['response']['docs'][arg]['url']
jpg：['data']['result']['response']['docs'][arg]['cover_path']
专辑主播名和主播url：
['data']['result']['response']['docs'][arg]['nickname']
['data']['result']['response']['docs'][arg]['anchorUrl']
进入专辑：
https://www.ximalaya.com/revision/play/album?albumId={}&pageNum={}&pageSize=30'.format(专辑,页码)
m4a:['data']['tracksAudioPlay'][arg]['src']
专辑名：['data']['tracksAudioPlay'][arg]['albumName']
m4a名字：name = ['data']['tracksAudioPlay'][arg]['trackName'].replace('|',',')
#主播url:'https://www.ximalaya.com/revision/user/?uid={16809064}'.format(zhubo_id)
'''
import re,requests
import threading

class Xmly:
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    def __init__(self,search_name,
                 url='https://www.ximalaya.com',
                 encode = 'utf-8',
                 ):
        self.s = requests.Session()
        self.search_name = search_name
        self.url = url
        self.encode = encode
        self.result = self.search_result()
        self.num = self.ypage()
    def search_result(self,page = 1):
        search_url = 'https://www.ximalaya.com/revision/search?core=album&kw={}&page={}&spellchecker=true&rows = 20'.format(self.search_name,page)
        print(search_url)
        result = self.s.get(search_url,headers = self.headers).json()
        result = result['data']['result']['response']
        return result
    def ypage(self):
        '''
        return: 搜索个数，页数；{'669':34}
        '''
        num = {}
        search_num = self.result['numFound']
        ypage = int(search_num)//20+1
        num['search_num'] = search_num
        num['ypage'] = ypage
        return num
    def ab_ypage(self,chapter_url):
        #返回页数
        ypage_url = 'https://www.ximalaya.com/revision/album?albumId={}'.format(chapter_url)
        ypage = self.s.get(ypage_url,headers = self.headers).json()
        ypage = int(ypage['data']['tracksInfo']['trackTotalCount']/30)+2
        return ypage
    def search_content(self):
        '''
        return: 这页所有搜索到的内容（669个）；{专辑链接：[名字,专辑img_url,专辑zhubo,专辑zhubo_url]}
        {'3335270': ['舞步学院约会公开课', 'http://imagev2.....jpg',
            '舞步学院情感', '16809064'],...}
        '''
        content = {}
        ypage = self.num['ypage']
        for x in range(int(ypage)):
            result = self.search_result(x+1)
            #print(result)
            resutlt_list = result['docs']
            #print(result['docs'])
            for i in resutlt_list:
                #print(i)
                name = i['title']
                name_url = i['url'].split('/')[2]
                try :
                    name_img = i['cover_path']
                except:
                    name_img = ''
                zhubo = i['nickname']
                zhubo_url = i['anchorUrl'].split('/')[2]
                content[name_url] = [name,name_img,zhubo,zhubo_url]
            #print(content)
        return content
    def album(self,ab_id):
        num = self.ab_ypage(ab_id)
        content = {}
        for i in range(num):
            ab_url = 'https://www.ximalaya.com/revision/play/album?albumId={}&pageNum={}&pageSize=30'.format(ab_id,i+1)
            print(ab_url)
            album_content = self.s.get(ab_url, headers=self.headers).json()
            for i in album_content['data']['tracksAudioPlay']:
                try:
                    m4a_name = i['trackName'].replace('|', ',')
                except:
                    m4a_name = i['trackName']
                m4a_url = i['src']
                content[m4a_url] = m4a_name
        return content
    def zhubo_ypage(self,zhubo_id):
        ypage_url = 'https://www.ximalaya.com/revision/user/track?page=1&pageSize=30&keyWord=&uid={}'.format(zhubo_id)
        ypage = self.s.get(ypage_url, headers=self.headers).json()
        ypage = int(ypage['data']['totalCount'])// 30 + 2
        return ypage
    def zhubo(self,zb_id):
        num = self.zhubo_ypage(zb_id)
        content = {}
        for i in range(num):
            zhubo_url = 'https://www.ximalaya.com/revision/user/track?page={}&pageSize=30&keyWord=&uid={}'.format(i,zb_id)
            zhubo_list = self.s.get(zhubo_url, headers=self.headers).json()
            for x in zhubo_list['data']['trackList']:
                #print(x)
                name = x['title']
                img_url = x['coverPath']
                name_url = x['albumUrl'].split('/')[2]
                content[name_url] = [name,img_url]
        #print(len(content))
        return content
if __name__ == '__main__':
    content = Xmly('舞步学院pua').zhubo('1000202') #search_content()album('3335270')
    print(content)