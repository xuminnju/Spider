from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pymysql

conn = pymysql.connect(host='localhost',port=3307,user='root',password='usbw',db='qzone',charset='utf8')
cursor = conn.cursor()
#使用selenium
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.maximize_window()
#登录QQ空间
def get_shuoshuo(qq):
    driver.get('http://user.qzone.qq.com/{}/311'.format(qq))
    time.sleep(5)
    try:
        driver.find_element_by_id('login_div')
        a = True
    except:
        a = False
    if a == True:
        driver.switch_to.frame('login_frame')
        driver.find_element_by_id('switcher_plogin').click()
        driver.find_element_by_id('u').clear()  # 选择用户名框
        driver.find_element_by_id('u').send_keys('290349938')
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys('999955132360xumi')
        driver.find_element_by_id('login_button').click()
        time.sleep(3)
    driver.implicitly_wait(3)
    try:
        driver.find_element_by_id('QM_OwnerInfo_Icon')
        b = True
    except:
        b = False
    if b == True:
        next_page = 'page'
        driver.switch_to.frame('app_canvas_frame')
        page = 1
        try:
            while next_page:
                content = driver.find_elements_by_css_selector('.content')
                stime = driver.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')
                for con, sti in zip(content, stime):
                    data = {
                        'time': sti.text,
                        'shuos': con.text
                    }
                    if con.text == '':
                        continue
                    print(data)
                    cursor.execute('INSERT INTO qq(time,shuoshuo)VALUES(%s,%s);',
                                   (sti.text,con.text))
                    conn.commit()
                page = page + 1
                print(u'正在抓取第%d页面内容······' % page)
                next_page = driver.find_element_by_link_text(u'下一页')
                next_page.click()
                time.sleep(3)
                driver.implicitly_wait(3)
        except:
            print(u'抓取到%d页面结束' % page)
    cookie = driver.get_cookies()
    cookie_dict = []
    for c in cookie:
        ck = "{0}={1};".format(c['name'], c['value'])
        cookie_dict.append(ck)
    i = ''
    for c in cookie_dict:
        i += c
    print('Cookies:', i)
    print("==========完成================")

    driver.close()
    driver.quit()



if __name__ == '__main__':
    get_shuoshuo('1141908319')
    cursor.close()
    conn.close()