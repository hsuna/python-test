import requests #导入requests 模块

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; WAS-AL00 Build/HUAWEIWAS-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044208 Mobile Safari/537.36 MicroMessenger/6.7.2.1340(0x2607023A) NetType/WIFI Language/zh_HK',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-HK,zh-HK;q=0.8,en-US;q=0.6'

}  #给请求指定一个请求头来模拟chrome浏览器

cookies={
    'SERVER_ID': '7daa0086-d03e44f61',
    'isvoted': 'MTY1NTcyMSwyMzE%3D',
    'headimgurl': 'http://thirdwx.qlogo.cn/mmopen/vi_32/asrTlSIsA5KmCoDxcdeRRKmOzBXRYtoMpepadhVqZ6AmrorTr7u5WW7sHjnbBiamf2q6ZotnrFGlnH6TtGp6jbA/132',
    'ptnickname': 'loading',
    'a08e175432b87f39': 'f1ac35c5ffd261df9f812b0b6e506de4_1789867_1537629240'
}

web_url = 'http://hapi.3k.com'

payload = {
    'ct': 'fssjh5',
    'ac': 'votes',
    'id': '0250',
    'from_id': '0',
    'game_id': '',
    'pf': '1',
    '_': '1537621599679',
    'signature': '873E1E186E1767D504D2F9B4B2D13E4C',
    'callback': 'jsonp_1537621599680_54985'
}

r = requests.get(web_url, params=payload, headers=headers, cookies=cookies) #像目标url地址发送get请求，返回一个response对象
print(r.text)
