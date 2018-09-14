import requests
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
        self.headers = { 
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", 
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
        }  #给请求指定一个请求头来模拟chrome浏览器
        self.tree_url = 'http://www.k-part.com/komatsu/komatsu/tree'  #要访问的网页地址
        self.page_url = 'http://www.k-part.com/komatsu/komatsu/page'  #要访问的网页地址
        self.img_url = 'http://free.komatsupartsbook.com/wm'
        self.folder_path = 'D:\Desktop\KPartData\json'  #设置存放的文件目录
        self.img_path = 'D:\Desktop\KPartData\img'  #设置存放的图片目录
        self.logs_path = 'D:\Desktop\KPartData\logs'  #设置存放的历史记录目录
        self.q = Queue() #线程
        self.THREADS_NUM = 10
    
    def working(self):
        while True:
            arguments = self.q.get()
            self.request_task(*arguments)
            self.q.task_done()

    def get_data(self):
        #创建文件夹
        self.mkdir(self.folder_path)
        self.mkdir(self.img_path)
        #添加历史记录路径
        self.mkdir(self.logs_path)
        time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.access_path = os.path.join(self.logs_path, 'access_'+time_str+'.log')
        self.error_path = os.path.join(self.logs_path, 'error_'+time_str+'.log')
        
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
            url = self.page_url
            data = {
                'book': book,
                'key': data["key"],
            }
        else:
            url = self.tree_url
            data = {
                'depth': depth,
                'book': book,
                'key': int(data["key"]),
                'sort': '[{"property":"sortBy","direction":"ASC"},{"property":"text","direction":"ASC"}]'
            }
        self.q.put((url, data))

    def request_task(self, url, data):
        path = os.path.join(self.folder_path, str(data["book"]))
        filename = str(data["key"])+'.json'
        filepath = os.path.join(path, filename)
        isExists = os.path.exists(filepath)
        if isExists:
            content = self.get_file(filepath)
        else:
            r = self.request(url, data)
            if r:
                content = r.text
                self.mkdir(path)#创建文件夹
                self.save_file(filepath, content)
            else:
                self.error('请求文件失败：', json.dumps(data))
                return


        if content:
            if 'tree' in url:
                items = json.loads(content)
                for item in items:
                    self.processing_data(item, data["depth"]+1)
            elif 'page' in url: #page
                rdata = json.loads(content)
                for img in rdata["image"]:
                    filepath = os.path.join(self.img_path, img.BookDir, img.PicName)
                    url = os.path.join(self.img_url, img.BookDir, img.PicName)
                    self.save_img(filepath, url)

        else:
            self.error('请求文件失败：', json.dumps(data))

    def get_file(self, filepath):
        try:
            f = open(filepath)
            content = f.read()
            f.close()
            #print('读取文件数据：', filepath)
            return content
        except Exception as e:
            return False
        finally:
            f.close()

    def save_file(self, filepath, content):
        print('开始保存文件数据')
        f = open(filepath, 'a+')
        f.write(content)
        self.log('文件保存成功：', filepath)
        f.close()
        return True

    def save_img(self, filepath, url):
        isExists = os.path.exists(filepath)
        if not isExists:
            img = self.request_img(url)
            if img:
                self.mkdir(path)#创建文件夹
                print('开始保存图片数据')
                f = open(filepath, 'ab')
                f.write(img.content)
                self.log('图片保存成功：', filename)
                f.close()
    
    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            print('创建', path, '文件夹')
            return True
        else:
            return False

    def log(self, *content):
        print(*content)
        f = open(self.access_path, 'a+')
        f.write("  ".join(content)+'\n')
        f.close()

    def error(self, *content):
        print(*content)
        f = open(self.error_path, 'a+')
        f.write("  ".join(content)+'\n')
        f.close()

    @retry(times=3)
    def request(self, url, data):
        try:
            r = requests.post(url, data=data, headers=self.headers, timeout=60)
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

    @retry(times=3)
    def request_img(self, url):
        try:
            r = requests.get(url, headers=self.headers, timeout=60)
            print('开始下载图片：', r.url)

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

""" r = kpart.request(kpart.page_url, {
    'book': 6155,
    'key': 5
})
rdata = json.loads(r.text)
print(rdata["image"]) """