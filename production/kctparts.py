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
        self.folder_path = 'D:\Desktop\KctpartsData'  #设置存放的文件目录
        self.access_path = '' #历史记录
        self.error_path = '' #错误记录
        self.q = Queue() #线程
        self.THREADS_NUM = 12
    
    def working(self):
        while True:
            arguments = self.q.get()
            self.save_task(arguments)
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
        #添加历史记录路径
        time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.access_path = os.path.join(self.folder_path, 'access_'+time_str+'.log')
        self.error_path = os.path.join(self.folder_path, 'error_'+time_str+'.log')

        all_a = BeautifulSoup(driver.page_source, 'lxml').select('a[href^="/#!hyundai-model"]')

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
            li_3 = a.find_parent('li').find_parent('li')
            li_2 = li_3.find_parent('li')
            li_1 = li_2.find_parent('li')

            id = a['href'].replace("/#!", "")

            lv_1 = li_1.span.get_text()
            lv_2 = li_2.span.get_text()
            lv_3 = li_3.span.get_text()
            lv_4 = a.get_text()
            data = self.request(id, "catalog/getModel", "application/json, text/javascript, */*; q=0.01")

            if data:
                data = json.loads(data.text)
                if isinstance(data, dict):
                    for key,values in data.items():
                        lv_5 = values["text"]
                        path = os.path.join(self.folder_path, lv_1, lv_2, lv_3, lv_4, lv_5)
                        self.mkdir(path)

                        for child in values["children"]:
                            spanSoup = BeautifulSoup(child["text"], 'lxml')
                            title = spanSoup.a.get_text()

                            id = spanSoup.span["id"]
                            file_name = id+'.json'
                            file_path = os.path.join(path, file_name) 
                            isExists = os.path.exists(file_path)
                            if not isExists:
                                self.q.put({
                                    "id":id, 
                                    "title":title, 
                                    "file_name":file_name, 
                                    "file_path":file_path
                                })
                            else:
                                self.log('文件已经存在：', file_path)
            else:
                self.error('请求文件失败：', id)
        
        #等待进程结束
        self.q.join()

    def save_task(self, map):
        file = self.request(map["id"], 'catalog/getSpares')
        file_path = map["file_path"]
        if file:
            print('开始解析文件')
            items = self.analy_file(file)
            content = json.dumps({
                'title': map["title"],
                'data': items
            })
            print('开始保存文件数据')
            f = open(file_path, 'a+')
            f.write(content)
            self.log('文件保存成功：', file_path)
            f.close()
        else:
            self.error('请求文件失败：', file_path)


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

    def analy_file(self, file):
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

        return items

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