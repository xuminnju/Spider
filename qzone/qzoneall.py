#coding:utf-8
from selenium import webdriver
import time,os
import re
import xlrd,xlwt
from xlutils.copy import copy
#使用selenium
#使用selenium的隐藏PhantimJS浏览器登陆账号后对内容获取
#注意frame与iframe的格式框切换
#driver = webdriver.PhantomJS(executable_path="E:\\mac\\id\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")

#driver.set_preference('network.proxy.type', 1)
#driver.set_preference('network.proxy.http', '127.0.0.1')
#driver.set_preference('network.proxy.http_port', 17890)
def get_shuoshuo(qq,path):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.maximize_window()
    try:
        driver.set_page_load_timeout(10)
        driver.get('http://user.qzone.qq.com/{}/311'.format(qq))
        time.sleep(3)
    except:
        print(u'网页启动异常，请重新打开')
        time.sleep(2)
        driver.quit()
    try:
        driver.find_element_by_id('login_div')
    except:
        print(u"非好友无法进入空间无权限抓取内容")
        driver.quit()
    else:
        #登录QQ空间
        driver.switch_to.frame('login_frame')
        driver.find_element_by_id('switcher_plogin').click()
        driver.find_element_by_id('u').clear()#选择用户名框
        driver.find_element_by_id('u').send_keys('290349938') #输入个人登录账号
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys('999955132360xumi') #输入个人登录密码
        driver.find_element_by_id('login_button').click()
        time.sleep(3)
    driver.implicitly_wait(3)
    try:
        driver.find_element_by_id('QM_OwnerInfo_Icon')
    except:
        print(u'空间加载异常，请重新打开')
        time.sleep(2)
        driver.quit()
    else:
        testexist(qq, path)
        driver.switch_to.frame('app_canvas_frame')
    #    last_page=driver.find_element_by_css_selector('.mod_pagenav')
    #    page_num=re.findall('\d+',last_page.text)[-1]
        next_page='page'
        page=1
        try:
            while next_page:
                content = driver.find_elements_by_css_selector('.content')
                stime = driver.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')
                for con,sti in zip(content,stime):
                    data = {
                        'time':sti.text,
                        'shuos':con.text
                    }
                    write_data(qq,data['time'],data['shuos'],path)
                next_page=driver.find_element_by_link_text(u'下一页')
                page=page+1
                print(u'正在抓取第%d页面内容······'%page)
                next_page.click()

                time.sleep(3)
                driver.implicitly_wait(3)
            driver.quit()
        except:
            print(u'抓取到%d页面结束'%page)
            driver.quit()

def  testexist(qq,path):
    if not os.path.exists(path):
        w= xlwt.Workbook()
        w.add_sheet(qq)
        w.save(path)
    else:
        os.remove(path)
        w= xlwt.Workbook()
        w.add_sheet(qq)
        w.save(path)

def write_data(qq,data1,data2,path):
    f=xlrd.open_workbook(path)
    sheet=f.sheet_by_name(qq)
    src=copy(f)
    row=sheet.nrows
    src.get_sheet(0).write(row,0,data1)
    src.get_sheet(0).write(row,1,data2)
    src.save(path)

if __name__ == '__main__':
    data = open(r'C:\Users\nimux\Desktop\qq.txt')
    for line in data:
        qq = re.match('([0-9]+)@qq.com', line)
        if qq:
            qq = ''.join(qq.groups(0))
            print(qq)
            work_path= 'D:\\0930\\{}.csv'.format(qq)
            get_shuoshuo(qq,work_path)#输入好友QQ号