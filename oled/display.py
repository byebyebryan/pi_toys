from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.core import lib

from luma.oled.device import sh1106

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from pins import Pins

# width = 128
# height = 64
# image = Image.new('1', (width, height))
# draw = ImageDraw.Draw(image)

serial = spi(device=0, port=0, bus_speed_hz=8000000,
             transfer_size=4096, gpio_DC=Pins.DC_PIN.value, gpio_RST=Pins.RST_PIN.value)
device = sh1106(serial, width=128, height=64, rotate=2)  # sh1106


def render(renderer):
    with canvas(device) as draw:
        renderer(draw)
