from selenium import webdriver  #导入Selenium
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup  #导入BeautifulSoup 模块
from urllib3.exceptions import NewConnectionError
from threading import Thread
from queue import Queue
import os  #导入os模块
import time
import json
import re

class retry(object):
    def __init__(self,*,times):
        self._cnt=times
    def __call__(self,func):
        def wrapper(*args,**kw):
            data=False
            cnt=self._cnt
            while data==False and cnt>0:
                data=func(*args,**kw)
                cnt-=1
            return data
        return wrapper

class KPartData():
    def __init__(self):  #类的初始化操作
        self.headers = { "Accept": "*/*", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "keep-alive", "Content-Length": "16", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Cookie": "PHPSESSID=dv3m7a1s7d5unfemr0t1vq6uh0; _ga=GA1.2.157321965.1536831013; _gid=GA1.2.2033674562.1536831013; __zlcmid=oNhdhBm8SQrRb2; language=62fb30aab70452488e110d403b8b36a8380957ccs%3A2%3A%22en%22%3B", "Host": "www.k-part.com", "Origin": "http://www.k-part.com", "Referer": "http://www.k-part.com/", "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36", "X-Requested-With": "XMLHttpRequest" }  #给请求指定一个请求头来模拟chrome浏览器
        self.tree_url = 'http://www.k-part.com/komatsu/komatsu/tree'  #要访问的网页地址
        self.page_url = 'http://www.k-part.com/komatsu/komatsu/page'  #要访问的网页地址
        self.folder_path = 'D:\Desktop\KPartData'  #设置存放的文件目录
        self.q = Queue() #线程
        self.THREADS_NUM = 10
    
    def working(self):
        while True:
            arguments = self.q.get()
            self.request_task(*arguments)
            self.q.task_done()

    def get_data(self):
        #创建主文件夹
        self.mkdir(self.folder_path)
        #添加历史记录路径
        self.error_path = os.path.join(self.folder_path, 'error_'+time.strftime("%Y%m%d%H%M%S", time.localtime())+'.log')
        
        #开启线程
        threads = []        
        for i in range(self.THREADS_NUM):
            t = Thread(target=self.working)#线程的执行函数为working
            threads.append(t)

        for item in threads:
            item.setDaemon(True)
            item.start()

        print('开始获取数据')
        self.q.put((self.tree_url, {
            'depth': 0,
            'book': '',
            'key': 0,
            'sort': '[{"property":"sortBy","direction":"ASC"},{"property":"text","direction":"ASC"}]',
            'node': 'root'
        }))

        #等待进程结束
        self.q.join()

    def processing_data(self, data, depth):
        book = data["book"] if "book" in data else ''
        if "leaf" in data and data["leaf"] == "1": #叶子，转去查询page
            url = self.page_url,
            data = {
                'book': book,
                'key': data["key"],
            }
        else:
            url = self.tree_url+'?_dc='+str(int(time.time()))
            data = {
                'depth': depth,
                'book': book,
                'key': data["key"],
                'sort': '[{"property":"sortBy","direction":"ASC"},{"property":"text","direction":"ASC"}]'
            }
        self.q.put((url, data))

    def request_task(self, url, data):
        r = self.request(url, data)
        if r:
            if 'tree' in url:
                items = json.loads(r.content)
                for item in items:
                    self.processing_data(item, data["depth"]+1)
            else:
                rdata = json.loads(r.content)
                self.save_file((data["book"], data["key"]), data["key"], r.content)
        else:
            self.error('请求文件失败：', *data)
            
    def save_file(self, path, filename, content):
        path = os.path.join(self.folder_path, path)
        self.mkdir(path)#创建文件夹
        os.chdir(path) #切换文件夹
        print('开始保存文件数据')
        f = open(filename, 'a+')
        f.write(content)
        self.save_log(filename, '文件保存成功：')
        f.close()
        return True
    
    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            print('创建', path, '文件夹')
            return True
        else:
            return False
            
    def error(self, *content):
        print(*content)
        f = open(self.error_path, 'a+')
        f.write("  ".join(content)+'\n')
        f.close()

    @retry(times=3)
    def request(self, url, data):
        try:
            r = requests.post(url, data=json.dumps(data), headers=self.headers, timeout=60)
            print('开始请求文件数据：', r.url, data)

            if r.status_code == 200:
                return r
            return False
        except requests.exceptions.ConnectTimeout:
            return False
        except requests.exceptions.Timeout:
            return False
        except Exception as e:
            return False


kpart = KPartData()  #创建类的实例
kpart.get_data()  #执行类中的方法