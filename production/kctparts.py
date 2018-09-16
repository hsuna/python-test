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

class KctpartsData():
    def __init__(self):  #类的初始化操作
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}  #给请求指定一个请求头来模拟chrome浏览器
        self.web_url = 'http://parts.kctparts.com/'  #要访问的网页地址
        self.folder_path = 'D:\Desktop\KctpartsData\data'  #设置存放的文件目录
        self.cache_path = 'D:\Desktop\KctpartsData\cache'  #设置缓存的文件目录
        self.log_path = 'D:\Desktop\KctpartsData\log'  #设置存放的文件目录
        self.access_path = '' #历史记录
        self.error_path = '' #错误记录
        self.q = Queue() #线程
        self.THREADS_NUM = 12
    
    def working(self):
        while True:
            arguments = self.q.get()
            self.queue_task(arguments)
            self.q.task_done()

    def get_data(self):
        print('开始网页get请求')
        # 使用selenium通过PhantomJS来进行网络请求
        #driver = webdriver.PhantomJS()

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        driver = webdriver.Chrome('D:\Software\Python\chromedriver_2.41.exe', chrome_options=chrome_options)  #指定使用的浏览器，初始化webdriver
        driver.get(self.web_url)
        print('访问成功')
        
        #创建主文件夹
        self.mkdir(self.folder_path)
        self.mkdir(self.cache_path)        
        self.mkdir(self.log_path)
        #添加历史记录路径
        time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.access_path = os.path.join(self.log_path, 'access_'+time_str+'.log')
        self.error_path = os.path.join(self.log_path, 'error_'+time_str+'.log')

        all_a = BeautifulSoup(driver.page_source, 'lxml').select('.folder > a[href^="/#!zf"]')
        #all_a = BeautifulSoup(driver.page_source, 'lxml').select('.folder > a[href^="/#!"]')

        name_rule = re.compile(r'[\/\\*:?<>"|]*')
        
        #开启线程
        threads = []        
        for i in range(self.THREADS_NUM):
            t = Thread(target=self.working)#线程的执行函数为working
            threads.append(t)

        for item in threads:
            item.setDaemon(True)
            item.start()
        
        for a in all_a:
            dirs = [a.get_text()]
            li = a.find_parent('li').find_parent('li')

            while hasattr(li, 'span'):
                dirs.insert(0, li.span.get_text())
                li = li.find_parent('li')
            
            self.q.put({
                "type": "list",
                "href":a['href'],
                "dirs": dirs
            })
        
        #等待进程结束
        self.q.join()

    def get_model_list(self, href, dirs):
        id = re.match(r'/#!(.*/)?([^/]*)', href).group(2)
        file_name = id.replace(":", "_")+'.json'
        file_path = os.path.join(self.cache_path, file_name)
        isExists = os.path.exists(file_path)
        if not isExists:
            data = self.request(id, "catalog/getModel", "application/json, text/javascript, */*; q=0.01")
            if data:
                content = data.text
                self.save_file(file_path, content)
        else:
            content = self.get_file(file_path)


        if content:
            data = json.loads(content)
            if isinstance(data, dict):
                for key,values in data.items():
                    t_dirs = dirs.copy()
                    t_dirs.append(values["text"])
                    self.get_model(values["children"], t_dirs)
                    
            elif isinstance(data, list):
                self.get_model(data, dirs)

        else:
            self.error('请求文件失败：', id)

    def get_model(self, children, dirs):
        for child in children:
            if "hasChildren" in child:
                a = BeautifulSoup(child["text"], 'lxml').a
                self.q.put({
                    "type": "list",
                    "href":a['href'],
                    "dirs": dirs
                })
            else:
                spanSoup = BeautifulSoup(child["text"], 'lxml')
                title = spanSoup.a.get_text()

                id = spanSoup.span["id"]
                file_name = id.replace(":", "_")+'.json'
                file_path = os.path.join(self.folder_path, file_name) 
                isExists = os.path.exists(file_path)
                if not isExists:
                    self.q.put({
                        "type": "file",
                        "id":id, 
                        "title":title,
                        "file_name":file_name, 
                        "file_path":file_path,
                        "dirs": dirs
                    })
                else:
                    print('文件已经存在：', file_path)

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
        try:
            print('开始保存文件数据')
            f = open(filepath, 'a+')
            f.write(content)
            self.log('文件保存成功：', filepath)
            f.close()
            return True
        except Exception as e:
            return False
        finally:
            f.close()

    def queue_task(self, data):
        if data["type"] == "file":
            file = self.request(data["id"], 'catalog/getSpares')
            file_path = data["file_path"]
            if file:
                print('开始解析文件')
                content = self.analy_spares(data, file)
                self.save_file(file_path, content)
            else:
                self.error('请求文件失败：', file_path)

        elif data["type"] == "list":
            self.get_model_list(data["href"], data["dirs"])

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

    def analy_spares(self, data, file):
        items = []
        table = BeautifulSoup(file.text, 'lxml').find(id='items_list').find('table')
        ths = table.select('thead th')
        trs = table.select('tbody tr')

        for tr in trs:
            tds = tr.find_all('td')
            td_len = len(tds)
            tmp = {}
            for i, th in enumerate(ths):
                if i < td_len:
                    tmp[th.get_text()] = tds[i].get_text()

            items.append(tmp)
            
        return json.dumps({
            'title': data["title"],
            'dirs': data["dirs"],
            'data': items
        })

    @retry(times=3)
    def request(self, node_id, r, accept="*/*"):
        try:
            headers = {
                'Accept': accept,
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Cookie': 'PHPSESSID=8p4rn22lhr5ukc49mta0qhqrp1; _ym_uid=1536831056995187252; _ym_d=1536831056; _ym_isad=2; _ym_visorc_30860931=w',
                'Host': 'parts.kctparts.com',
                'Referer': 'http://parts.kctparts.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
            }

            r = requests.get('http://parts.kctparts.com/', params={
                "r": r,
                "node_id": node_id
            }, headers=headers, timeout=60)
            print('开始请求文件数据：', node_id)

            if r.status_code == 200:
                return r
            return False
        except requests.exceptions.ConnectTimeout:
            return False
        except requests.exceptions.Timeout:
            return False
        except Exception as e:
            return False


    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            print('创建', path, '文件夹')
            return True
        else:
            return False



kctparts = KctpartsData()  #创建类的实例
kctparts.get_data()  #执行类中的方法