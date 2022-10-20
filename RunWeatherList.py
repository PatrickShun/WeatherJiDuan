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
        self.UnixTime = int(time.time()) * 1000     # 获取当前Unix时间
        self.weatherCityCoordinate = []             # 预制空列表，用于存储天气信息
        self.weatherCLASS = "05"                    # 自定义定义极端天气
        self.requestsNUM = 5                        # 自定义请求次数（eg:仅打印出前5个）
        self.skycon = {'CLEAR_DAY': '晴（白天）', 'CLEAR_NIGHT': '晴（夜间）', 'PARTLY_CLOUDY_DAY': '多云（白天）',
                       'PARTLY_CLOUDY_NIGHT': '多云（夜间）', 'CLOUDY': '阴', 'LIGHT_HAZE': '轻度雾霾(PM2.5 100~150)',
                       'MODERATE_HAZE': '中度雾霾(PM2.5 150~200)', 'HEAVY_HAZE': '重度雾霾(PM2.5 > 200)',
                       'LIGHT_RAIN': '小雨', 'MODERATE_RAIN': '中雨', 'HEAVY_RAIN': '大雨', 'STORM_RAIN': '暴雨',
                       'FOG': '雾', 'LIGHT_SNOW': '小雪', 'MODERATE_SNOW': '中雪', 'HEAVY_SNOW': '大雪',
                       'STORM_SNOW': '暴雪', 'DUST': '浮尘', 'SAND': '沙尘', 'WIND': '大风'}

    def GetUrlData(self):
        # 获取极端天气数据,紧接着自动保存到本地
        # BaseURL = "http://www.weather.com.cn/alarm/alarm_list.shtml"
        BaseURL = "http://product.weather.com.cn/alarm/grepalarm_cn.php?_=" + str(self.UnixTime)
        print(BaseURL)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        req = urllib.request.Request(BaseURL, headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode('utf-8')
        # print(html)
        self.SaveData(html)

    def SaveData(self, html):
        f = open("weatherList.txt", 'w+', encoding="utf-8")
        f.write(html[14:-1])
        print("正在保存......")
        f.close()
        time.sleep(2)

    def readDateFile(self):
        print("读取本地text文档")
        with open("weatherList.txt", 'r', encoding='utf-8') as f:
            data1 = json.load(f)
            cityList = data1['data']
            for clo in range(1, 5):
                for i in cityList:
                    color = "-" + self.weatherCLASS + "0" + str(clo)
                    if color in i[1]:
                        print(i[0], i[2], i[3])
                        self.weatherCityCoordinate.append(i[:-2])
                    # else:
                    #     print("未找到天气")
            print("查找完毕！")

    def GetCaiyunAPI(self, coordinate):
        """https://api.caiyunapp.com/v2.5/EofNoB9Agjjvgtw5/104.061514,30.642986/realtime"""
        CaiyunGetURL = "https://api.caiyunapp.com/v2.5/EofNoB9Agjjvgtw5/" + coordinate + "/realtime"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        time.sleep(2)
        try:
            req = urllib.request.Request(CaiyunGetURL, headers=headers)
            res = urllib.request.urlopen(req)
            html = res.read().decode('utf-8')
            data1 = json.loads(html)
            # print(data1['result'])
            # visibility = (data1['result']['realtime']['visibility'])
            return data1
        except:
            print('GetCaiyunAPI 出错了！')

    def run(self):
        access = 0                                  # 用于限制请求次数，提高效率，每次运行清零。
        self.GetUrlData()                           # 获取国家天气预警信息并下载数据
        self.readDateFile()                         # 读取下载下来的数据
        for i in self.weatherCityCoordinate:        # 遍历下载的数据
            if access == self.requestsNUM:          # 如果请求彩云天气的次数等于设定的次数，则停止运行。
                break
            iCoordinate = str(i[2]) + "," + str(i[3])
            data2 = self.GetCaiyunAPI(iCoordinate)
            access += 1
            result_skycon = data2['result']['realtime']['skycon']
            skycon = self.skycon[result_skycon]
            print("=" * 50)
            print(" 城市：     \t{}".format(i[0]))
            print(" 经纬度：   \t{}".format(iCoordinate))
            print(" 天气现象：  \t{}".format(skycon))
            print(" 温度：     \t{}℃".format(data2['result']['realtime']['temperature']))
            print(" 能见度：   \t{}Km".format(data2['result']['realtime']['visibility']))
            print(" 湿度：     \t{}%".format(data2['result']['realtime']['humidity'] * 100))
            print(" 风：       \t风速：{}\t风向：{}".format(data2['result']['realtime']['wind']['speed'],
                                                        data2['result']['realtime']['wind']['direction']))
            print(" AQI指数：  \t{}\t{}".format(data2['result']['realtime']['air_quality']['aqi']['chn'],
                                              data2['result']['realtime']['air_quality']['description']['chn']))
            # print(" 紫外线指数：\t{}".format(data2['result']['realtime']['life_index']))
            print("=" * 50, "\n")

        print("Done!")


if __name__ == "__main__":
    print("Beginning!")
    weatherList = WeatherList()
    weatherList.run()
