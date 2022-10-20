# WeatherJiDuan
获取极端天气经纬度，使用彩云API获取天气详细信息





# Caiyun docs
# 天气现象(skycon)
主要天气现象的优先级：降雪 > 降雨 > 雾 > 沙尘 > 浮尘 > 雾霾 > 大风 > 阴 > 多云 > 晴

天气现象	代码	备注
晴（白天）	CLEAR_DAY	cloudrate < 0.2
晴（夜间）	CLEAR_NIGHT	cloudrate < 0.2
多云（白天）	PARTLY_CLOUDY_DAY	0.8 >= cloudrate > 0.2
多云（夜间）	PARTLY_CLOUDY_NIGHT	0.8 >= cloudrate > 0.2
阴	CLOUDY	cloudrate > 0.8
轻度雾霾	LIGHT_HAZE	PM2.5 100~150
中度雾霾	MODERATE_HAZE	PM2.5 150~200
重度雾霾	HEAVY_HAZE	PM2.5 > 200
小雨	LIGHT_RAIN	见 降水强度
中雨	MODERATE_RAIN	见 降水强度
大雨	HEAVY_RAIN	见 降水强度
暴雨	STORM_RAIN	见 降水强度
雾	FOG	能见度低，湿度高，风速低，温度低
小雪	LIGHT_SNOW	见 降水强度
中雪	MODERATE_SNOW	见 降水强度
大雪	HEAVY_SNOW	见 降水强度
暴雪	STORM_SNOW	见 降水强度
浮尘	DUST	AQI > 150, PM10 > 150，湿度 < 30%，风速 < 6 m/s
沙尘	SAND	AQI > 150, PM10> 150，湿度 < 30%，风速 > 6 m/s
大风	WIND	
