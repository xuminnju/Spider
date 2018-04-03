import requests
from bs4 import BeautifulSoup
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
html = requests.get('http://www.weather.com.cn/weather/101220501.shtml', headers = headers).content
soup = BeautifulSoup(html, 'lxml')
times = soup.select('ul.t > li.sky > h1')
weathers = soup.select('ul.t > li.sky > p.wea')
temps = soup.select('ul.t > li.sky > p.tem')
winds = soup.select('ul.t > li.sky > p.win')
for time,weather,temp,wind in zip(times,weathers,temps,winds):
    data = {
        '时间':time.get_text().strip(),
        '天气':weather.get_text().strip(),
        '温度':temp.get_text().strip(),
        '风力':wind.get_text().strip()
    }
    print(data)