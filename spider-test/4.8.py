from selenium import webdriver  #导入Selenium
import requests
from bs4 import BeautifulSoup  #导入BeautifulSoup 模块
import os  #导入os模块
import time
import re

class OPComic():
    def __init__(self):  #类的初始化操作
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}  #给请求指定一个请求头来模拟chrome浏览器
        self.web_url = 'https://www.fzdm.com/manhua/002//'  #要访问的网页地址
        self.folder_path = 'D:\Desktop\ONE_PIECE'  #设置图片要存放的文件目录

    def get_pic(self):
        print('开始创建文件夹')
        is_new_folder = self.mkdir(self.folder_path)  #创建文件夹，并判断是否是新创建

        req = self.request(self.web_url)
        all_a = BeautifulSoup(req.text, 'lxml').select('.pure-u-1-2 a')
        a = all_a[0]

        for a in all_a:
            sava_path = os.path.join(self.folder_path, a['title'])
            self.mkdir(sava_path)
            print('切换子文件夹', sava_path)
            os.chdir(sava_path)   #切换路径至上面创建的文件夹

            page = 1
            start_url = next_url = self.web_url+a['href']
            while next_url:
                req = self.request(next_url)
                result = re.search(r'var ?mhurl="([^"]*)"', req.text)
                if result:
                    url = 'http://p0.xiaoshidi.net/' + result.group(1)
                    self.save_img(url, str(page)+'.jpg')  # 调用save_img方法来保存图片

                result = re.search(r'"#mhimg0"\)\.html\(\'<a href="([^"]*)">', req.text)
                if result:
                    next_url = start_url + result.group(1)
                else:
                    next_url = False
                page += 1

    def save_img(self, url, file_name): ##保存图片
        print('开始请求图片地址，过程会有点长...')
        img = self.request(url)
        print('开始保存图片')
        f = open(file_name, 'ab')
        f.write(img.content)
        print(file_name,'图片保存成功！')
        f.close()

    def request(self, url):  #返回网页的response
        r = requests.get(url)  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
        return r

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print('创建名字叫做', path, '的文件夹')
            os.makedirs(path)
            print('创建成功！')
            return True
        else:
            print(path, '文件夹已经存在了，不再创建')
            return False

comic = OPComic()  #创建类的实例
comic.get_pic()  #执行类中的方法