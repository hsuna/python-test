from urllib.parse import urlparse
 
result = urlparse('http://www.baidu.com/index.html;user?id=5&test=abc#comment')
print(type(result), result)