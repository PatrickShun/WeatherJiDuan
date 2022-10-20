import urllib.request
import json

"""https://api.caiyunapp.com/v2.5/EofNoB9Agjjvgtw5/104.061514,30.642986/realtime"""

CaiyunGetURL = "https://api.caiyunapp.com/v2.5/EofNoB9Agjjvgtw5/104.061514,30.642986/realtime"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

req = urllib.request.Request(CaiyunGetURL,headers=headers)
res = urllib.request.urlopen(req)
html = res.read().decode('utf-8')
data1 = json.loads(html)

# print(html['result'])
print(data1['result']['realtime']['visibility'])