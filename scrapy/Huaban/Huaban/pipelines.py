# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os  #导入os模块
import requests
import winreg
import logging

class HuabanPipeline(object):
    def __init__(self):
        self.headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        }
        self.save_path = os.path.join(self.get_desktop(), 'huaban')
        self.mkdir(self.save_path)

    def process_item(self, item, spider):
        dir_path = os.path.join(self.save_path, item['imgDir'])
        self.mkdir(dir_path)

        file_path = os.path.join(dir_path, item['imgName']+item['imgType'].replace('image/', '.'))
        isExists = os.path.exists(file_path)
        if not isExists:
            img = self.request_img(item['imgUrl'])
            if img:
                print('开始保存图片数据')
                f = open(file_path, 'ab')
                f.write(img.content)
                f.close()
                logging.info('保存图片成功['+file_path+']')
            else:
                print('下载图片失败', item['imgUrl'])


        return item

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            logging.info('创建名字叫做['+path+']的文件夹')
            return True
        else:
            return False

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
    
    def get_desktop(self):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        return winreg.QueryValueEx(key, "Desktop")[0]