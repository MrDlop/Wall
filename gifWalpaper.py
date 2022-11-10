import sys

from PIL import Image
import ctypes
import os.path
from asyncio import sleep, run
infile = 'girl.gif'

try:
    im = Image.open(infile)
except IOError:
    print("Cant load", infile)
    sys.exit(1)

i = 0

try:
    while 1:
        im2 = im.convert('RGBA')
        im2.load()

        background = Image.new("RGB", im2.size, (255, 255, 255))
        background.paste(im2, mask=im2.split()[3])
        background.save('g/girl' + str(i) + '.jpg', 'JPEG', quality=80)

        i += 1
        im.seek(im.tell() + 1)

except EOFError:
    pass

path = r"g"


async def start():
    while True:
        for address, dirs, files in os.walk(path):
            for name in files:
                ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.join(address, name), 0)
                await sleep(0.01)


run(start())
