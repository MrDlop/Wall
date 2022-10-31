import ctypes
import os.path
from asyncio import sleep, run

path = r"resurse/iloveimg-converted"

async def start():
    while True:
        for address, dirs, files in os.walk(path):
            for name in files:
                ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.join(address, name), 0)
                await sleep(0.1)


run(start())
