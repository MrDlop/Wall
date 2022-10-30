from asyncio import sleep, run
from sqlite3 import connect
from requests import get
from ctypes import windll
from subprocess import Popen, PIPE

import config


async def start():
    while True:
        con = connect('bd')
        cur = con.cursor()
        home = cur.execute(f"""SELECT * FROM homeInfo""").fetchall()[0]
        path = 'resurse/weather.jpg'
        if home[5] == 0:
            if home[3]:
                data = get(f"http://api.openweathermap.org/data/2.5/weather?"
                           f"q={home[0]}&type=like&APPID={config.appid}").json()
                weather = data['weather'][0]['main']
            else:
                data = get(f"http://api.openweathermap.org/data/2.5/weather?"
                           f"lat={home[1]}&lon={home[2]}&type=like&APPID={config.appid}").json()
                weather = data['weather'][0]['main']
            path = cur.execute(f"""SELECT path FROM pathToImage WHERE title='{weather}'""").fetchall()[0][0]
            con.close()
        elif home[5] == 1:
            cmd = 'python telegramGeneratePhoto.py'
            p = Popen(cmd, stdout=PIPE, shell=True)
            p.wait()

        windll.user32.SystemParametersInfoW(20, 0, path, 0)
        await sleep(home[4])


run(start())
