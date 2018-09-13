from selenium import webdriver  #导入Selenium
import requests
from bs4 import BeautifulSoup  #导入BeautifulSoup 模块
from urllib3.exceptions import NewConnectionError
import os  #导入os模块
import time
import json
import re

class KctpartsData():
    def __init__(self):  #类的初始化操作
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}  #给请求指定一个请求头来模拟chrome浏览器
        self.web_url = 'http://parts.kctparts.com/'  #要访问的网页地址
        self.folder_path = 'D:\Desktop\KctpartsData'  #设置图片要存放的文件目录

    def get_data(self):
        print('开始网页get请求')
        # 使用selenium通过PhantomJS来进行网络请求
        #driver = webdriver.PhantomJS()
        driver = webdriver.Chrome('D:\Software\Python\chromedriver_2.41.exe')  #指定使用的浏览器，初始化webdriver
        driver.get(self.web_url)
        #self.scroll_down(driver=driver, times=5)  #执行网页下拉到底部操作，执行5次
        print('开始获取tree')
        
        all_a = BeautifulSoup(driver.page_source, 'lxml').select('a[href^="/#!hyundai-model"]')

        name_rule = re.compile(r'[\/\\*:?<>"|]*')
        
        for a in all_a:
            li_3 = a.find_parent('li').find_parent('li')
            li_2 = li_3.find_parent('li')
            li_1 = li_2.find_parent('li')

            id = a['href'].replace("/#!", "")

            lv_1 = li_1.span.get_text().replace(' ', "_")
            lv_2 = li_2.span.get_text().replace(' ', "_")
            lv_3 = li_3.span.get_text().replace(' ', "_")
            lv_4 = a.get_text().replace(' ', "_")
            data = self.request(id, "catalog/getModel", "application/json, text/javascript, */*; q=0.01")

            if data:
                data = json.loads(data.text)
                for key,values in data.items():
                    lv_5 = values["text"].replace(' ', "_")
                    print(self.folder_path, lv_1, lv_2, lv_3, lv_4, lv_5)
                    path = os.path.join(self.folder_path, lv_1, lv_2, lv_3, lv_4, lv_5)
                    self.mkdir(path)
                    os.chdir(path) #切换文件夹

                    for child in values["children"]:
                        spanSoup = BeautifulSoup(child["text"], 'lxml')
                        name = spanSoup.a.get_text().replace(' ', "_")
                        name = re.sub(name_rule, '', name)+'.json'

                        id = spanSoup.span["id"]
                        self.save_file(id, os.path.join(name))

    def save_file(self, id, file_name):
        file = self.request(id, 'catalog/getSpares')
        if file:
            print('开始解析文件')
            content = self.analy_file(file)
            print('开始保存文件数据')
            f = open(file_name, 'a+')
            f.write(content)
            print(file_name, '文件保存成功！')
            f.close()

    def analy_file(self, file):
        items = []
        table = BeautifulSoup(file.text, 'lxml').find(id='items_list').find('table')
        ths = table.select('thead th')
        trs = table.select('tbody tr')

        for tr in trs:
            tds = tr.find_all('td')
            tmp = {}
            for i, th in enumerate(ths):
                if th.get_text().replace('\u00a0', "") != "":
                    tmp[th.get_text()] = tds[i].get_text()

            items.append(tmp)

        return json.dumps(items)

    def request(self, node_id, r, accept="*/*"):
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

        try:
            r = requests.get('http://parts.kctparts.com/', params={
                "r": r,
                "node_id": node_id
            }, headers=headers)
            print('开始请求文件数据：', node_id)

            if r.status_code == 200:
                return r
        
        except Exception as e:
            print('请求文件失败：', node_id)

        return False

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            print('创建', path, '的文件夹')
            return True
        else:
            return False



kctparts = KctpartsData()  #创建类的实例
kctparts.get_data()  #执行类中的方法