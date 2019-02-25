from enum import Enum

from gpiozero import Button

from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.core import lib

from luma.oled.device import sh1106

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from RPi import GPIO


class Pins(Enum):
        RST_PIN = 25
        CS_PIN = 8
        DC_PIN = 24
        JOYSTICK_UP_PIN = 6
        JOYSTICK_DOWN_PIN = 19
        JOYSTICK_LEFT_PIN = 5
        JOYSTICK_RIGHT_PIN = 26
        JOYSTICK_CENTER_PIN = 13
        KEY_1_PIN = 21
        KEY_2_PIN = 20
        KEY_3_PIN = 16


class Device:
    
    def __init__(self, *args, **kwargs):
        self.width = 128
        self.height = 64

        self.serial = spi(device=0,
                          port=0,
                          bus_speed_hz=8000000,
                          transfer_size=4096,
                          gpio_DC=Pins.DC_PIN.value,
                          gpio_RST=Pins.RST_PIN.value)
        self.display = sh1106(self.serial,
                              width=self.width,
                              height=self.height,
                              rotate=2)

        self.joystick_up = Button(Pins.JOYSTICK_UP_PIN.value)
        self.joystick_down = Button(Pins.JOYSTICK_DOWN_PIN.value)
        self.joystick_left = Button(Pins.JOYSTICK_LEFT_PIN.value)
        self.joystick_right = Button(Pins.JOYSTICK_RIGHT_PIN.value)
        self.joystick_center = Button(Pins.JOYSTICK_CENTER_PIN.value)
        self.button_1 = Button(Pins.KEY_1_PIN.value)
        self.button_2 = Button(Pins.KEY_2_PIN.value)
        self.button_3 = Button(Pins.KEY_3_PIN.value)

    def __del__(self):
        GPIO.setmode(GPIO.BCM)

    def clear(self):
        self.display.clear()

    def getEmptyImage(self):
        return Image.new('1', (self.width, self.height))

    def display(self, image):
        self.display.display(image)

    def getCanvas(self):
        return canvas(self.display)

    def cleanup(self):
        self.display.cleanup()
