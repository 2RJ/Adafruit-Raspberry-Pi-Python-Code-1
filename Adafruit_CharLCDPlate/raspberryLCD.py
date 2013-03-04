#!/usr/bin/python

from time import sleep
import os
from Adafruit_I2C import Adafruit_I2C
from Adafruit_MCP230xx import Adafruit_MCP230XX
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

import smbus

def status():
	# initialize the LCD plate
	# use busnum = 0 for raspi version 1 (256MB) and busnum = 1 for version 2
	lcd = Adafruit_CharLCDPlate(busnum = 1)

	# clear display
	lcd.clear()
	lcd.backlight(lcd.GREEN)



	stat_fd = open('/proc/stat')
	stat_buf = stat_fd.readlines()[0].split()

	prev_total = float(stat_buf[1]) + float(stat_buf[2]) + float(stat_buf[3]) + float(stat_buf[4]) + float(stat_buf[5]) + float(stat_buf[6]) + float(stat_buf[7])
	prev_idle = float(stat_buf[4])
	stat_fd.close()
	sleep(3)
	while 1:

		stat_fd = open('/proc/stat')
		stat_buf = stat_fd.readlines()[0].split()
		total = float(stat_buf[1]) + float(stat_buf[2]) + float(stat_buf[3]) + float(stat_buf[4]) + float(stat_buf[5]) + float(stat_buf[6]) + float(stat_buf[7])
		idle = float(stat_buf[4])
		stat_fd.close()
		diff_idle = idle - prev_idle
		diff_total = total - prev_total
		usage = 1000.0 * (diff_total - diff_idle) / diff_total
		usage = usage / 10
		usage = round(usage, 1)
		prev_total = total
		prev_idle = idle
		lcd.clear()
		lcd.message('CPU:'+ repr(usage) + '%')
		for n in range(1,3):
			if( lcd.buttonPressed(lcd.SELECT)):
				return 0
			sleep(1)
			
			
if __name__ == '__main__':
	status()
