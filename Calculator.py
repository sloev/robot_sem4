'''
Created on 21/11/2013

@author: Ivo
'''
import time 
import RPi.GPIO as gpio
from random import randrange
from fileinput import input


class Calculator():
    
    gpio.setmode(gpio.BOARD) 
    gpio.setup(16, gpio.OUT)
    gpio.setup(26, gpio.OUT)
    gpio.setup(12, gpio.OUT)

    def __init__(self):
        self.wrong = 0
        self.correct = 0   
        
        
    def add(self):
        a = randrange(10)
        b = randrange(10)
        print('What is ' + str(a) + ' + ' + str(b))
        answer = raw_input("Enter your answer: ")
        answer = int(answer)
        realAnswer = a + b
        if(answer==realAnswer):
            print('Correct')
            self.correct+=1
            gpio.output(16,True)
            gpio.output(12,True)
            time.sleep(1)
            gpio.output(16,False)
            gpio.output(12,False)
        else:
            print('Wrong')
            self.wrong+=1
            self.totallyWrong()         
            
            
    def subtract(self):
        a = randrange(10)
        b = randrange(10)
        print("what is" + str(a) + " - " + str(b))
        answer = raw_input("enter your answer: ")
        answer = int(answer)
        realanswer = a - b
        if(answer==realanswer):
            print("correct")
            self.correct+=1
        else:
            print("wrong")
            self.wrong+=1
            
            gpio.output(26,False)
            gpio.output(16,False)
                    
    def pow(self):
        a = randrange(12)
        print("what is: " + str(a) + " ^ " + str(2))
        realanswer =pow(a,2)
        answer = raw_input("enter your answer")
        answer = int(answer)
        if(answer==realanswer):
            print("correct")
            self.correct+=1
        else:
            print("wrong")
            self.wrong+=1
 
 
    def multiply(self):
        a = randrange(10)
        b = randrange(10)
        print("what is" +str(a) + " * "  + str(b))
        realanswer = a * b
        answer = raw_input("enter your answer")
        answer = int(answer)
        if(answer==realanswer):
            print("correct")
            self.correct+=1
        else:
            print("wrong")
            self.wrong+=1
            
          
    def divide(self):
        a = randrange
        b = randrange
        print("what is" + str(a) + " / " + str(b))
        realanswer = a / b
        answer = raw_input("enter your answer")
        answer = int(answer)
        if(answer==realanswer):
            print("correct")
            self.correct+=1
        else:
            print("wrong")
            self.wrong+=1
            
            
    def totallyWrong(self):
        gpio.output(26,True)
        for i in range(1000):
            gpio.output(12,True)
            time.sleep(0.0001)
            gpio.output(12,False)
            time.sleep(0.0001)
        gpio.output(26,False)
                
    
    def calculations(self):
        
        print("Welcome to Daniel Hansen calculator!")
        print(" ")
        number = raw_input("How many calculations do you want?")
        number = int(number)
        print("1: addition")
        print("2: subtraction")
        print("3: multiplication")
        print("4: division")
        print("5: pow")
        print(" ")
        choice = raw_input("Enter your choice: ")
        choice = int(choice)
         
        if(choice==1):
            for i in range(number):
                self.add()
        elif(choice==2):
            for i in range(number):
                self.subtract()
        elif(choice==3):
            for i in range(number):
                self.multiply()
        elif(choice==4):
            for i in range(number):
                self.divide()
        elif(choice==5):
            for i in range(number):
                self.pow()                
        else:
            print("Invalid number!")
        
        print("you had "+str(self.correct)+" correct answers")
        print("you had "+str(self.wrong)+" wrong answers")
                
    
def main():
    calculater=Calculator()
    calculater.calculations()
    
if __name__ == '__main__':
    main()
        