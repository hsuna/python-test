import imghdr
from bs4 import BeautifulSoup  #导入BeautifulSoup 模块
import os  #导入os模块
from threading import Thread
from queue import Queue
import time

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

class HuabanPicture():
    def __init__(self):  #类的初始化操作
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}  #给请求指定一个请求头来模拟chrome浏览器
        self.web_url = 'http://login.meiwu.co/login'  #要访问的网页地址
        self.folder_path = 'D:\Desktop\Huaban'  #设置图片要存放的文件目录
        self.q = Queue() #线程
        self.THREADS_NUM = 12
        #self.driver = webdriver.PhantomJS() # 使用selenium通过PhantomJS来进行网络请求
        self.driver = webdriver.Chrome('D:\Software\Python\chromedriver_2.41.exe')  #指定使用的浏览器，初始化webdriver

    def working(self):
        while True:
            arguments = self.q.get()
            self.save_img(arguments)
            self.q.task_done()

    def login_user(self):
        print('开启线程', self.THREADS_NUM)
        #开启线程
        threads = []        
        for i in range(self.THREADS_NUM):
            t = Thread(target=self.working)#线程的执行函数为working
            threads.append(t)

        for item in threads:
            item.setDaemon(True)
            item.start()

        #创建文件夹
        self.mkdir(self.folder_path)

        print('开始网页get请求')
        self.driver.get(self.web_url)
        self.driver.find_element_by_css_selector('input[name="email"]').send_keys()
        time.sleep(1)
        self.driver.find_element_by_css_selector('input[name="password"]').send_keys()
        time.sleep(1)
        self.driver.find_element_by_css_selector('a#submit').click()

        time.sleep(3)
        self.driver.get(self.driver.current_url+'?jra00000&limit=10000&wfl=1')       

        selector = BeautifulSoup(self.driver.page_source, 'lxml')
        links = selector.select('#waterfall div .link')

        for link in links:
            self.parse_boards({
                "url": 'http://login.meiwu.co' + link["href"].strip()
            })

        #等待进程结束
        self.q.join()

    def parse_boards(self, data):
        self.driver.get(data["url"])
        selector = BeautifulSoup(self.driver.page_source, 'lxml')

        dir_path = selector.select('h1.board-name')[0].get_text().strip()
        dir_path = os.path.join(self.folder_path, dir_path)
        self.mkdir(dir_path)

        links = selector.select('#waterfall div a.loaded.img')
        for link in links:
            self.parse_pins({
                "dir_path": dir_path,
                "url": 'http://login.meiwu.co' + link["href"].strip()
            })


    def parse_pins(self, data):
        self.driver.get(data["url"])
        selector = BeautifulSoup(self.driver.page_source, 'lxml')

        file_name = selector.select('div[data-id]')[0]["data-id"].strip()
        file_path = os.path.join(data["dir_path"], file_name) 
        
        url = 'http:' + selector.select('div[data-img]')[0]["data-img"].strip()
        self.q.put({
            "file_path": file_path,
            "url": url
        })

    def save_img(self, data):
        print(data)
        url = data['url']
        file_path = data['file_path']
        isExists = os.path.exists(file_path)
        if not isExists:
            img = self.request_img(url)
            if img:
                print('开始保存图片数据')
                f = open(file_path, 'ab')
                f.write(img.content)
                f.close()

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



huaban = HuabanPicture()  #创建类的实例
huaban.login_user()  #执行类中的方法
