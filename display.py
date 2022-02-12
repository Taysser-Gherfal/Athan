#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in7
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

def updateDisplay():
    try:

        logging.info("epd2in7 Demo")   
        epd = epd2in7.EPD()
        
        '''2Gray(Black and white) display'''
        logging.info("init and Clear")
        epd.init()
        epd.Clear(0xFF)
        font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
        font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
        font50 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 50)
        # Drawing on the Horizontal image
        logging.info("1.Drawing on the Horizontal image...")
        Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        draw.text((10, 0), 'Next Prayer', font = font18, fill = 0)   
        draw.text((10, 30), 'Fajer', font = font50, fill = 0)
        draw.text((10, 95), '06:30 am', font = font50, fill = 0)
        draw.text((10, 160), '---------------------- 02/11/2022 ----------------------', font = font12, fill = 0)     
        epd.display(epd.getbuffer(Himage))
        epd.sleep()
            
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd2in7.epdconfig.module_exit()
        exit()
