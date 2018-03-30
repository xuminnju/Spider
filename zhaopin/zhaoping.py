# coding:utf-8
import requests
from bs4 import BeautifulSoup
import threading
from multiprocessing import Pool
import time
import pymysql

conn = pymysql.connect(host='localhost',port=3307,user='root',password='usbw',db='zhaopin',charset='utf8')
cursor = conn.cursor()

def get_zhaopin(page):
    url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%8D%97%E4%BA%AC&kw=python&sm=0&sg=c745e7d236d14e7f9b46c75f7fbfde63&p={0}'.format(page)
    print("第{0}页".format(page))
    wbdata = requests.get(url).content
    soup = BeautifulSoup(wbdata,'lxml')
    job_name = soup.select("table.newlist > tr > td.zwmc > div > a")
    salarys = soup.select("table.newlist > tr > td.zwyx")
    locations = soup.select("table.newlist > tr > td.gzdd")
    times = soup.select("table.newlist > tr > td.gxsj > span")
    for name, salary, location, time in zip(job_name, salarys, locations, times):
        data = {
            'name': name.get_text().strip(),
            'salary': salary.get_text(),
            'location': location.get_text(),
            'time': time.get_text()
        }
        print(data)
        cursor.execute('INSERT INTO data(name, salary, location, time)VALUES(%s,%s,%s,%s);', (name.get_text().strip(),salary.get_text(),location.get_text(),time.get_text()))
        conn.commit()

if __name__ == '__main__':
    starttime = time.time()
    pool = Pool(processes=8)
    pool.map_async(get_zhaopin, range(1,18))
    pool.close()
    pool.join()
    print(time.time()-starttime)
    cursor.close()
    conn.close()