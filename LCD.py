# -*- coding: utf-8 -*

import time

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import fcntl
import struct
import socket
import subprocess
import os

# Get Serial
def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"
  return cpuserial

# CPU Temperature
def getCPUtemperature():
        Temp = os.popen('vcgencmd measure_temp').readline()
        return(Temp.replace("temp=","Temperature: ").replace("'C\n","\xB0C"))

# V core
def getVoltage():
        Voltage = os.popen('vcgencmd measure_volts core').readline()
        return (Voltage.replace("volt=","Volt: ").replace("V\n"," V"))

# IP Address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 0))
ip = s.getsockname()[0]

# hostname
hostname = (socket.gethostname())

# Mac Address
def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' % ord(char) for char in info[18:24]])

# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

# Hardware SPI usage:
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))
# Initialize library.
disp.begin(contrast=60)

# Clear display.
disp.clear()
disp.display()


while True:
        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
        
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        
        # Draw a white filled box to clear the image.
        draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
        
        # Load default font.
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 7)

        # Write mac text.
        draw.text((1,1), 'mac:', font=font)
        draw.text((20,1), getHwAddr('wlan0'), font=font)
        
        # Wirte ip text.
        draw.text((1,8), 'ip:', font=font)
        draw.text((11,8), ip, font=font)
        
        # Write Temperature text.
        draw.text((1,15), getCPUtemperature(), font=font)
        
        # Write hostname text.
        draw.text((1,22), 'host:', font=font)
        draw.text((20,22), hostname, font=font)
        
        # Write Serial text.
        draw.text((1,29), 'SN:', font=font)
        draw.text((14,29), getserial(), font=font)

        # Write core text.
        draw.text((1,36), getVoltage(), font=font)
        

        # Display image.
        disp.image(image)
        disp.display()
        
        time.sleep(0.5)
