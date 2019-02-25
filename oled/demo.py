# -*- coding:utf-8 -*-

# from luma.core.interface.serial import i2c, spi
# from luma.core.render import canvas
# from luma.core import lib

# from luma.oled.device import sh1106
# import RPi.GPIO as GPIO

from device import Device
# from display import render

import time
import subprocess
from signal import pause

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from RPi import GPIO

import socket

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()

    width = 128
    height = 64

    padding = 0
    top = padding
    bottom = height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0
    y = 0

    font = ImageFont.truetype('../fonts/pixelmix.ttf', 8)

    d = Device()

    with d.getCanvas() as draw:
        draw.text((x, y), ip, font=font, fill=255)
        draw.text((x, 32), "this is a very long sentence", font=font, fill=255)

    pause()
except KeyboardInterrupt:
    print("exit")
    pass