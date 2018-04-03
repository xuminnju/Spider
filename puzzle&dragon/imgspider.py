import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

headers = {
    "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
url = 'http://puzzledragonx.com/en/monsterbook.asp'
html = requests.get(url).text
soup = BeautifulSoup(html,'lxml')
numList = soup.select('td.index > div.indexframe > div.iframenum')
List =[]
for i,val in enumerate(numList[:4266]):
    numList[i] = val.get_text()
    #print(numList[i])

def get_img(num):
    try:
        url = 'http://puzzledragonx.com/en/img/monster/MONS_%s.jpg'%num
        imgbyte = requests.get(url, headers=headers).content
        path = r'img/%s.png'%num
        with open(path,'wb') as fn:
            fn.write(imgbyte)
            print('%s号宠物图片已下载好'%num)
    except:
        print('下载失败')

for num in numList[4266]:
    get_img(num)
