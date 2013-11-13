'''
Created on 13/11/2013

@author: Ivo
'''
import RPi.GPIO as GPIO 
import time 

GPIO.setup(12, GPIO.OUT)

def Blink(numTimes):
    for i in range(0,numTimes):
        GPIO.output(12, True) ## Turn on LED 
        time.sleep(0.15)
        GPIO.output(12, False) ## Turn off LED
        time.sleep(0.15)
    print "MAAAAAAAAAAXXXX LOL"

iterations = raw_input("Enter the total number of times to blink: ")

Blink(int(iterations))