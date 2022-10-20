import time
import urllib.request
import urllib.parse
import json


# 1.先获取unix的实时时间 or 转换当前时间
# 2.仅获取一次，保存到本地，后续直接查本地数据（格式化处理，字典）
# 3.查询本地预警列表，筛选出需要的数据，如经纬度。
# 4.使用经纬度调用彩云天气API，获取此坐标的天气数据
# 5.封装可视化UI，集成筛选条件功能，输出极端天气的数据。
# ================
# 【天气类型+预警等级】
# 台风：01
# 暴雨：02
# 暴雪：03
# 寒潮：04
# 大风：05
# 沙尘暴：06
# 高温：07
# 干旱：08
# 雷电：09
# 冰雹：10
# 霜冻：11
# 大雾：12
# 霾：13
# 道路结冰：14
# 森林火灾：15
# 雷雨大风：16
# ================
# 蓝色预警：01
# 黄色预警：02
# 橙色预警：03
# 红色预警：04
# ================


class WeatherList(object):
    """用于获取天气极端天气的数据，数据来源于国家预警网站[http://www.weather.com.cn/alarm/alarm_list.shtml]"""

    def __init__(self):
        # 获取当前Unix时间
        self.UnixTime = int(time.time())*1000
        self.weatherCityCoordinate = []
        

    def GetUrlData(self):
        # 获取极端天气数据,紧接着自动保存到本地
        # BaseURL = "http://www.weather.com.cn/alarm/alarm_list.shtml"
        BaseURL = "http://product.weather.com.cn/alarm/grepalarm_cn.php?_=" + str(self.UnixTime)
        print(BaseURL)
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        req = urllib.request.Request(BaseURL,headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode('utf-8')
        # print(html)
        self.SaveData(html)


    def SaveData(self,html):
        # 保存获取到的极端天气数据
        f = open("weatherList.txt", 'w+',encoding="utf-8")
        f.write(html[14:-1]) # 只保留data数据，以及去掉最后的分号
        print("正在保存......")
        f.close()
        time.sleep(2)


    def readDateFile(self):
        # 读取本地Text文件,以及筛选条件，获取地方名称和经纬度。
        print("读取本地text文档")
        with open("weatherList.txt",'r',encoding='utf-8') as f:
            data1 = json.load(f)
            cityList = data1['data']
            for i in cityList:
                if "-0702" in i[1]: # 修改这个地方,对应不同天气!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!【前是极端天气，后是预警颜色】
                    # print(i[0],i[2],i[3])
                    self.weatherCityCoordinate.append(i[:-2])
                # else:
                #     print("未找到天气")
            print("查找完毕！")


    def GetCaiyunAPI(self,coordinate):
        """https://api.caiyunapp.com/v2.5/EofNoB9Agjjvgtw5/104.061514,30.642986/realtime"""
        CaiyunGetURL = "https://api.caiyunapp.com/v2.5/EofNoB9Agjjvgtw5/" + coordinate + "/realtime"
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        time.sleep(2)
        req = urllib.request.Request(CaiyunGetURL,headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode('utf-8')
        data1 = json.loads(html)

        # print(data1['result'])
        # visibility = (data1['result']['realtime']['visibility'])
        return data1


    def run(self):
        access = 0 # 用于限制请求次数，提高效率。
        # 获取并下载数据
        self.GetUrlData()

        # 读取数据
        self.readDateFile()
        for i in self.weatherCityCoordinate:
            if access == 2:
                break
            iCoordinate = str(i[2]) +","+ str(i[3])
            data2 = self.GetCaiyunAPI(iCoordinate)
            print("==============================")
            print("城市：" , i[0])
            print("经纬度：" + iCoordinate)
            print("温度：" , data2['result']['realtime']['temperature'])
            # print("能见度：",data2['result']['realtime']['visibility'])
            # print("湿度：",data2['result']['realtime']['humidity'])
            # print("风：",data2['result']['realtime']['wind'])
            # print("AQI指数：",data2['result']['realtime']['air_quality'])
            # print("紫外线指数：",data2['result']['realtime']['life_index'])



            access += 1
            print("==============================")

        print("Done!")


if __name__ == "__main__":
    print("Beginning!")
    weatherList = WeatherList()
    weatherList.run()

