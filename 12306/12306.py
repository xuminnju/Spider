#_*_ utf-8 _*_
import urllib,urllib2
import ssl
import cookielib

c = cookielib.LWPCookieJar()
cookie = urllib2.HTTPCookieProcessor(c)
opener = urllib2.build_opener(cookie)
headers = {
    "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
ssl._create_default_https_context = ssl._create_unverified_context

def login():
    req = urllib2.Request('https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.760187340911989')
    req.headers = headers
    codeimg = opener.open(req).read()
    with open('code.png', 'wb') as fn:
        fn.write(codeimg)

    req2 = urllib2.Request('https://kyfw.12306.cn/passport/captcha/captcha-check')
    req2.headers = headers
    code = raw_input('input code:')
    data = {
        "answer": code,
        "login_site": "E",
        "rand": "sjrand"
    }
    print(data)
    data = urllib.urlencode(data)
    html = opener.open(req2,data).read()
    print(html.decode('utf-8'))

    req3 = urllib2.Request('https://kyfw.12306.cn/passport/web/login')
    req3.headers = headers
    data = {
        'username': 'xuminnju',
        'password': 'xuyiming',
        'appid': 'otn'
    }
    data = urllib.urlencode(data)
    html = opener.open(req3, data).read()
    print(html.decode('utf-8'))

if __name__ == '__main__':
    login()