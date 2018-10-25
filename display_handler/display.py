import os
import subprocess
import redis
import time

import Adafruit_SSD1306
from mpu6050 import mpu6050
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


RST = None     # on the PiOLED this pin isnt used

disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
sensor = mpu6050(0x68)
# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
# font = ImageFont.load_default()
# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('font.ttf', 12)

currentDisplayText = ""
isConnected = False
# Define a client to connect to the local redis instance
redisClient = redis.StrictRedis()
redisPubSub = redisClient.pubsub(ignore_subscribe_messages=True)

# Subscribe to the display text value
redisPubSub.subscribe('disp.text')


def setDisplayText():
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    # Display image.
    draw.text((x, top), currentDisplayText, font=font, fill=255)
    disp.image(image)
    disp.display()


while True:
        # Query for new display text
    newDispText = redisPubSub.get_message(
        ignore_subscribe_messages=True,
        timeout=0.5,
    )
    # If we have a new string to put on the screen, and it isn't the same as the current one, set it
    if newDispText and newDispText['data'] != currentDisplayText:
        print("textUpdateEvent: " + newDispText['data'])
        currentDisplayText = newDispText['data']
        setDisplayText()

    # if we're connected but we think we aren't update.
    if redisClient.exists("heartbeat"):
        if not isConnected:
            isConnected = True
            setDisplayText()
            print("reconnection event. isConnected changing to True")
    # if we're disconnected but we think we are update
    else:
        if isConnected:
            isConnected = False
            setDisplayText()
            print("disconnection event. isConnected changing to False")
