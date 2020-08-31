from selenium import webdriver  #导入Selenium
import requests
from bs4 import BeautifulSoup  #导入BeautifulSoup 模块
import os  #导入os模块
import time

class KXFiction():
    def __init__(self):  #类的初始化操作
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}  #给请求指定一个请求头来模拟chrome浏览器
        self.web_url = 'https://m.boluoxs.com'  #要访问的网页地址
        self.folder_path = 'D:\Desktop\quanzhigaoshou.txt'  #设置图片要存放的文件目录

    def start(self):
        f = open(self.folder_path, 'ab')
        f.seek(0)
        f.truncate()   #清空文件
        
        page = 1
        while page <= 44:
            while True:
                try: 
                    req = self.request(self.web_url + '/59/59611_' + str(page) + '/')
                    all_a = BeautifulSoup(req.text, 'lxml').select('ul.lb.fk a.xbk')
                    if len(all_a) > 0:
                        break
                except Exception as e:
                    print(e)
                    pass

            for a in all_a:
                
                while True:
                    try: 
                        req = self.request(self.web_url + a['href'])
                        text = req.content.decode('gb18030', 'ignore')
                        soup = BeautifulSoup(text, 'lxml')
                        
                        #抓取文章标题
                        title = soup.select('#header .zhong')
                        tm = title[0].get_text().strip()

                        #抓取文章内容
                        content = soup.select('#nr')
                        nr = content[0].get_text()
                        break
                    except Exception as e:
                        print(e)
                        pass
            
                txt = '\t' + tm + '\r\n\r\n' + nr + '\r\n\r\n'
                f.write(txt.encode('utf-8'))
                print(tm)
            
            page = page + 1
            
        f.close()
    
    def request(self, url):  #返回网页的response
        r = requests.get(url, headers=self.headers)  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
        r.encoding = 'utf-8' 
        return r

comic = KXFiction()  #创建类的实例
comic.start()  #执行类中的方法