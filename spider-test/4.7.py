from selenium import webdriver  #导入Selenium
import requests
from bs4 import BeautifulSoup  #导入BeautifulSoup 模块
import os  #导入os模块
import time

class KXFiction():
    def __init__(self):  #类的初始化操作
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}  #给请求指定一个请求头来模拟chrome浏览器
        self.web_url = 'https://m.80txt.com'  #要访问的网页地址
        self.folder_path = 'D:\Desktop\kuangxu.txt'  #设置图片要存放的文件目录

    def start(self):
        f = open(self.folder_path, 'ab')
        f.seek(0)
        f.truncate()   #清空文件

        page = '/83440/27218555.html'
        while len(page) > 6:
            req = self.request(self.web_url + page)
            soup = BeautifulSoup(req.text, 'lxml')
            #抓取文章标题
            tag = soup.find('h1',id='_bqgmb_h1')
            title = tag.get_text()
            #抓取文章内容
            tag = soup.find('div',id='nr1')
            nr = tag.get_text()
            txt = '\t' + title + '\r\n\r\n' + nr + '\r\n\r\n'
            f.write(txt.encode('utf-8'))

            next = soup.find('a',id='pt_next')
            print(page, title)

            page = next['href']
            
        f.close()
    
    def request(self, url):  #返回网页的response
        r = requests.get(url)  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
        r.encoding = 'utf-8' 
        return r



comic = KXFiction()  #创建类的实例
comic.start()  #执行类中的方法