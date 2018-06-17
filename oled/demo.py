		# -*- coding:utf-8 -*-

from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.core import lib

from luma.oled.device import sh1106
import RPi.GPIO as GPIO

import time
import subprocess

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Load default font.
font = ImageFont.truetype('game_over.ttf', 32)

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = 128
height = 64
image = Image.new('1', (width, height))

# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

RST = 25
CS = 8		
DC = 24

USER_I2C = 0

if  USER_I2C == 1:
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(RST,GPIO.OUT)	
	GPIO.output(RST,GPIO.HIGH)
	
	serial = i2c(port=1, address=0x3c)
else:
	serial = spi(device=0, port=0, bus_speed_hz = 8000000, transfer_size = 4096, gpio_DC = 24, gpio_RST = 25)

device = sh1106(serial, rotate=2) #sh1106  

counter = 0;
start_time = 0;
draw_start_time = 0;

#try:
while True:
	with canvas(device) as draw:
	
		start_time = time.time()
		draw_time = start_time - draw_start_time
		
		#draw.rectangle(device.bounding_box, outline="white", fill="black")
		#draw.text((30, 40), "Hello World", fill="white")
		
		# Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
		
		#cmd = "hostname -I | cut -d\' \' -f1"
		#IP = subprocess.check_output(cmd, shell = True )
		#draw.text((x, top),       "IP: " + str(IP),  font=font, fill=255)
		
		#cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
		#CPU = subprocess.check_output(cmd, shell = True, universal_newlines=True )
		#draw.text((x, top+16),     str(CPU), font=font, fill=255)
		
		#cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
		#MemUsage = subprocess.check_output(cmd, shell = True, universal_newlines=True )
		#draw.text((x, top+32),    str(MemUsage),  font=font, fill=255)
		
		#cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
		#Disk = subprocess.check_output(cmd, shell = True )
		#draw.text((x, top+48),    str(Disk),  font=font, fill=255)
		
		counter += 1
		
		draw_start_time = time.time()
		
		draw.text((x, top),    "{}".format(counter),  font=font, fill=255)
		draw.text((x, top+16),    "proc {:.2f} : draw {:.2f}".format(draw_start_time - start_time, draw_time),  font=font, fill=255)
#except:
#	print("except")
GPIO.cleanup()
