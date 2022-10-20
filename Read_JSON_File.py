import json

# data1 = {
#     'no' : 1,
#     'name' : 'Runoob',
#     'url' : 'http://www.runoob.com'}

# json_str = json.dumps(data1)
# print("原始数据：",repr(data1))
# print("JSON对象",json_str)

# data2 = json.loads(json_str)
# print("data2-name:",data2['name'])
# print("data2-url:",data2['url'])


with open("weatherList.txt", 'r', encoding='utf-8') as f:
    data1 = json.load(f)
    print(data1['data'][2])

