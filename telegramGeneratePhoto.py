from ctypes import windll
from sqlite3 import connect

from requests import get
from sys import exit

import config

from telethon import TelegramClient, events

# Use your own values from my.telegram.org
api_id = config.api_id
api_hash = config.api_hash

client = TelegramClient('anon', api_id, api_hash)

con = connect('bd')
cur = con.cursor()
home = cur.execute(f"""SELECT * FROM homeInfo""").fetchall()[0]
if home[3]:
    data = get(f"http://api.openweathermap.org/data/2.5/weather?"
               f"q={home[0]}&type=like&APPID={config.appid}").json()
    weather = data['weather'][0]['description']
else:
    data = get(f"http://api.openweathermap.org/data/2.5/weather?"
               f"lat={home[1]}&lon={home[2]}&type=like&APPID={config.appid}").json()
    weather = data['weather'][0]['description']
con.close()


async def send_message():
    await client.send_message('@sber_rudalle_xl_bot', weather)


@client.on(events.NewMessage(chats='@sber_rudalle_xl_bot'))
async def normal_handler(event):
    if event.message.photo:
        await event.message.download_media("resurse/weather.jpg")
        if home[5]:
            windll.user32.SystemParametersInfoW(20, 0, "resurse/weather.jpg", 0)
        exit()


client.start()
client.loop.run_until_complete(send_message())
client.run_until_disconnected()
