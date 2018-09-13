from selenium import webdriver  #导入Selenium
import requests
from bs4 import BeautifulSoup  #导入BeautifulSoup 模块
from urllib3.exceptions import NewConnectionError
import os  #导入os模块
import time
import json

class ModelData():
    def __init__(self):
        self.headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': 'PHPSESSID=8p4rn22lhr5ukc49mta0qhqrp1; _ym_uid=1536831056995187252; _ym_d=1536831056; _ym_isad=2; _ym_visorc_30860931=w',
            'Host': 'parts.kctparts.com',
            'Referer': 'http://parts.kctparts.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.web_url = 'http://parts.kctparts.com/'
    def get_data(self, id, accept="*/*"):
        headers = self.headers
        headers['Accept'] = accept

        try:
            response = requests.get(self.web_url, params={
                "r": "catalog/getModel",
                "node_id": id
            }, headers=headers)
            print('读取数据：'+response.url)

            if response.status_code == 200:
                return response.text
        
        except Exception as e:
            print('超时')

        return None


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
        
        #response = requests.get(self.web_url, headers=self.headers)
        #all_a = BeautifulSoup(response.text, 'lxml').select('a[href^="/#!hyundai-model"]')

        tree = []
        
        for a in all_a:
            li_3 = a.find_parent('li')
            li_2 = li_3.find_parent('li')
            li_1 = li_2.find_parent('li')

            id = a['href'].replace("/#!", "")

            lv_1 = li_1.span.get_text(),
            lv_2 = li_2.span.get_text(),
            lv_3 = li_3.span.get_text(),
            lv_4 = a.get_text()
            
            model = ModelData()
            data = model.get_data(id, "application/json, text/javascript, */*; q=0.01")

            if data:
                data = json.loads(data)
                for key,values in data.items():
                    lv_5 = values["text"]

                    for child in values["children"]:
                        spanSoup = BeautifulSoup(child["text"], 'lxml')
                        lv_6 = spanSoup.a.get_text()

                        id = spanSoup.span["id"]
                        subas = ModelData()
                        data = subas.get_data(id)
                        if data:
                            #tableSoup = BeautifulSoup(data, 'lxml').select('#items_list table')

                            tree.append({
                                'lv_1': lv_1,
                                'lv_2': lv_2,
                                'lv_3': lv_3,
                                'lv_4': lv_4,
                                'lv_5': lv_5,
                                'lv_6': lv_6,
                                'table': data,
                            }) 
                    
        return tree

kctparts = KctpartsData()  #创建类的实例
tree = kctparts.get_data()  #执行类中的方法

f = open('test1.json','w')
f.write(json.dumps(tree))
f.close()

