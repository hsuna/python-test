import urllib.request

url="https://www.zhihu.com/question/29372574"
response=urllib.request.urlopen(url)

print(response.read().decode('utf-8'))