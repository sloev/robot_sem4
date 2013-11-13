'''
Created on 13/11/2013

@author: Ivo
'''
import RPi.GPIO as GPIO
import os

GPIO.setup(15,GPIO.IN)

print "Press button"

while True:
  if (GPIO.input(15)):
    os.system("sudo python /home/pi/robot_sem4/Button_Led/led.py")