#!/usr/bin/python

from time import sleep
import os
from Adafruit_I2C import Adafruit_I2C
from Adafruit_MCP230xx import Adafruit_MCP230XX
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate;

import smbus



class CPU(object):
	def __init__(self):
		"""Init a CPU status object"""
		stat_fd = open('/proc/stat')
		stat_buf = stat_fd.readlines()[0].split()

		self.prev_total = float(stat_buf[1]) + float(stat_buf[2]) + float(stat_buf[3]) + float(stat_buf[4]) + float(stat_buf[5]) + float(stat_buf[6]) + float(stat_buf[7])
		self.prev_idle = float(stat_buf[4])
		stat_fd.close()

	def usage(self):
		"""return the actual usage of cpu (in %)"""	
		stat_fd = open('/proc/stat')
		stat_buf = stat_fd.readlines()[0].split()
		total = float(stat_buf[1]) + float(stat_buf[2]) + float(stat_buf[3]) + float(stat_buf[4]) + float(stat_buf[5]) + float(stat_buf[6]) + float(stat_buf[7])
		idle = float(stat_buf[4])
		stat_fd.close()
		diff_idle = idle - self.prev_idle
		diff_total = total - self.prev_total
		usage = 1000.0 * (diff_total - diff_idle) / diff_total
		usage = usage / 10
		usage = round(usage, 1)
		self.prev_total = total
		self.prev_idle = idle
		return usage

def status(lcd, updateWait = 3, color = 0x02): #0x02 = GREEN
	# initialize the LCD plate
	# use busnum = 0 for raspi version 1 (256MB) and busnum = 1 for version 2
	
	# clear display
	lcd.clear()
	lcd.backlight(color)

	cpu = CPU()

	sleep(updateWait)

	while 1:

		lcd.clear()
		lcd.message('CPU:'+ repr( cpu.usage() ) + '%')
		for n in range(updateWait):
			if( lcd.buttonPressed(lcd.SELECT)):
				return 0
			sleep(1)
			
			
if __name__ == '__main__':

	lcd = Adafruit_CharLCDPlate(1)
	status(lcd, 3, lcd.GREEN)
