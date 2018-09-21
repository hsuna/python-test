from urllib3.exceptions import NewConnectionError
from threading import Thread
from queue import Queue
import os  #导入os模块
import time
import json
import re

class KctpartsData():
    def __init__(self):  #类的初始化操作
        self.clean_path = 'D:\Desktop\KctpartsClean\clean'  #设置存放的文件目录
        self.save_path = 'D:\Desktop\KctpartsClean\clean2'  #设置清理后的文件目录
        self.log_path = 'D:\Desktop\KctpartsClean\log'  #设置存放的文件目录
        self.access_path = '' #历史记录
        self.error_path = '' #错误记录
        self.q = Queue() #线程
        self.THREADS_NUM = 12
    
    def working(self):
        while True:
            arguments = self.q.get()
            self.queue_task(arguments)
            self.q.task_done()

    def clean_data(self):
        #创建主文件夹
        self.mkdir(self.save_path)
        self.mkdir(self.log_path)
        #添加历史记录路径
        time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.access_path = os.path.join(self.log_path, 'access_'+time_str+'.log')
        self.error_path = os.path.join(self.log_path, 'error_'+time_str+'.log')

        
        #开启线程
        threads = []        
        for i in range(self.THREADS_NUM):
            t = Thread(target=self.working)#线程的执行函数为working
            threads.append(t)

        for item in threads:
            item.setDaemon(True)
            item.start()
        
        print('开始遍历所有文件')
        files = os.listdir(self.clean_path) #得到文件夹下的所有文件名称
        for file in files:
            if not os.path.isdir(file):
                file_path = os.path.join(self.clean_path, file)
                self.q.put({
                    "file": file,
                    "path": file_path
                })
        
        
        #等待进程结束
        self.q.join()
        self.log('数据清理完成！！！')

    def queue_task(self, data):
        file_name = data["file"]
        file_path = data["path"]
        save_path = os.path.join(self.save_path, file_name)
        
        isExists = os.path.exists(save_path)
        if isExists:
            print('文件已经存在：', save_path)
        else:
            content = self.get_file(file_path)
            if content:
                data = json.loads(content)
                title = data["title"].lower()
                if re.match(r"[\S\s]+cylinder", title):
                    sealkits = []
                    for line in data["data"]:
                        description = line["Description"].lower().replace(" ", "")
                        if "sealkit" == description:
                            sealkits.append(line["Part #"])
                    if len(sealkits)>0:
                        data["sealkits"] = sealkits
                        content = json.dumps(data).replace("\\u00a0", "")
                        self.save_file(save_path, content)
                        return

                print('非匹配文件：', file_name)
            else:
                self.error('文件内容读取失败：', file_name)
            
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
kctparts.clean_data()  #执行类中的方法