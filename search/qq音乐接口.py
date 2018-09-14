
import requests

url = 'http://www.douqq.com/qqmusic/qqapi.php'
data = {
    'mid':'0025jqbO3zF1Gq'
    }


r = requests.get(url,data = data)

print(r.text)
