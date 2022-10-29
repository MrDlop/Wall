from ctypes import windll
from requests import get
import config


def replaceImageForWorkTable(path):
    windll.user32.SystemParametersInfoW(20, 0, path, 0)


def weatherNowCity(s_city):
    try:
        data = get(f"http://api.openweathermap.org/data/2.5/weather?"
                   f"q={s_city}&type=like&APPID={config.appid}").json()
        return data['weather'][0]['main']
    except Exception as e:
        return False


def weatherNowCoords(x, y):
    try:
        data = get(f"http://api.openweathermap.org/data/2.5/weather?"
                   f"lat={x}&lon={y}&type=like&APPID={config.appid}").json()
        return data['weather'][0]['main']
    except Exception as e:
        return False
