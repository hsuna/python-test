import requests
from bs4 import BeautifulSoup  #导入BeautifulSoup 模块

def parse_url_to_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    body = soup.find_all(class_="x-wiki-content")[0]
    html = str(body)
    with open("a.html", 'wb') as f:
        f.write(html)