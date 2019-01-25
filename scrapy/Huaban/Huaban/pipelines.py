# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from Huaban.settings import IMAGES_STORE
import os  #导入os模块
import requests

class HuabanPipeline(object):
    def __init__(self):
        self.headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        }
        self.mkdir(IMAGES_STORE)

    def process_item(self, item, spider):

        dir_path = os.path.join(IMAGES_STORE, item['imgDir'])
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
            else:
                print('下载图片失败', item['imgUrl'])


        return item

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print('创建名字叫做', path, '的文件夹')
            os.makedirs(path)
            print('创建成功！')
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