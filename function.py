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
    except Exception:
        return False


def weatherNowCoords(x, y):
    try:
        data = get(f"http://api.openweathermap.org/data/2.5/weather?"
                   f"lat={x}&lon={y}&type=like&APPID={config.appid}").json()
        return data['weather'][0]['main']
    except Exception:
        return False


def findCity(s_city):
    return len(get(f"http://api.openweathermap.org/data/2.5/find?"
                   f"q={s_city}&type=like&APPID={config.appid}").json()['list'])


def findCityForCoords(x, y):
    return len(get(f"http://api.openweathermap.org/data/2.5/find?"
                   f"lat={x}&lon={y}&type=like&APPID={config.appid}").json()['list'])


def infoCity(s_city):
    data = get(f"http://api.openweathermap.org/data/2.5/weather?"
               f"q={s_city}&type=like&APPID={config.appid}").json()
    return data


def infoCoords(x, y):
    data = get(f"http://api.openweathermap.org/data/2.5/weather?"
               f"lat={x}&lon={y}&type=like&APPID={config.appid}").json()
    return data
