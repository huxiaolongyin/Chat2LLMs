import json
import requests
from core.config import CONFIG
from core.utils import find_city_code


def get_current_weather(city_name: str) -> str:
    """获取天气信息"""
    key = CONFIG.API_KEY
    if not city_name:
        ip_get_url = f"https://restapi.amap.com/v3/ip?key={key}"
        response = requests.get(ip_get_url)
        if response.status_code == 200:
            city_code = response.json()['adcode']
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

tools = [{
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "仅在用户明确询问天气、温度、降水、气温等气象信息时使用。获取指定城市的当前天气情况。",
            "parameters": {
                "type": "object",
                "properties": {
                    "city_name": {
                        "type": "string",
                        "description": "中国城市的名称，如果不指定则会返回空值",
                    },
                },
                "required": ["city_name"],
            },
        },
    }]
