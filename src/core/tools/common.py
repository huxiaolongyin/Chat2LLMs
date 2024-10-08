import json
import requests
from datetime import datetime
from core.config import CONFIG
from core.utils import find_city_code


def get_current_weather(city_name: str) -> str:
    """获取城市当前的天气信息"""
    key = CONFIG.GAODE_API_KEY
    if not city_name:
        ip_get_url = f"https://restapi.amap.com/v3/ip?key={key}"
        response = requests.get(ip_get_url)
        if response.status_code == 200:
            city_code = response.json()["adcode"]
        else:
            return "获取位置信息失败"
    else:
        city_code = find_city_code(city_name)

    url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={key}&city={city_code}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        weather_info = data["lives"][0]
        return json.dumps(weather_info, ensure_ascii=False)
    else:
        return "获取天气信息失败"


def get_current_time():
    """获取当前时间"""
    return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
