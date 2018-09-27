import requests
import re

class Ip:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    def __init__(self):
        self.get_list = self.get_list()
    def get_list(self):
        daili = requests.get("http://www.xicidaili.com/nn/",headers=self.headers)
        daili.encoding = 'utf-8'
        daili_text = daili.text
        regex = '<td>(.*?)</td>'
        daili_c = re.findall(regex,daili_text)
        daili_list = []
        for i in daili_c[::5]:
            daili_list.append(i)
        return daili_list
    def get_can_ip(self):
        get_list = self.get_list
        for i in get_list:
            ip = i  # 代理ip    国内高级代理ip:http://www.xicidaili.com/nn
            proxies = {"http": i, "https": i, }
            try:
                res = requests.get("http://2018.ip138.com/ic.asp", proxies=proxies, headers=self.headers)
            except:
                pass
            else:
                res.encoding = 'gb2312'
                regex = '<body style="margin:0px"><center>(.*?)</center></body>'
                huoqu = re.findall(regex, res.text)
                if len(huoqu) != 0:
                    break
                else:
                    print('下一个')
                    pass
        print(i)
        return i

def proxies():
  get_ip = Ip().get_can_ip()
  proxies = {"http": get_ip, "https": get_ip, }
  return proxies

print(proxies())




'''
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
ip = '116.1.11.19'  #代理ip    国内高级代理ip:http://www.xicidaili.com/nn
proxies = {"http": ip,"https": ip,}
res = requests.get("http://2018.ip138.com/ic.asp",proxies = proxies,headers = headers)
res.encoding = 'gb2312'
regex = '<body style="margin:0px"><center>(.*?)</center></body>'
#print(re.findall(regex,res.text))
'''