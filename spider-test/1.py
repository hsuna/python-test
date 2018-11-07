""" import urllib.request

url="https://www.zhihu.com/question/29372574"
response=urllib.request.urlopen(url)

print(response.read().decode('utf-8')) """

def test(*param):
    print("".join(param))

def test2(id, file_name, title):
    print(id, file_name, title)

test("1","2","3")